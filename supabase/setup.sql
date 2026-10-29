-- V5. Sistema de preinscripción deportiva (ENTORNO EXCLUSIVO DE PRUEBAS).
-- Ejecutar una sola vez en Supabase > SQL Editor.
-- No habilitar inscripción pública de usuarios. Crear cuentas de prueba en Auth > Users.
-- Claves de acceso y usuarios reales jamás deben incluirse en GitHub.

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null default 'Usuario/a de prueba',
  role text not null check (role in ('profesor','ind'))
);

-- Función con privilegios protegidos para comprobar el rol sin recursión RLS.
create or replace function public.is_ind_admin()
returns boolean
language sql stable security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.profiles p
    where p.id = (select auth.uid()) and p.role = 'ind'
  );
$$;
revoke all on function public.is_ind_admin() from public, anon;
grant execute on function public.is_ind_admin() to authenticated;

-- Solo las cuentas con perfil aprobado como profesor pueden ingresar registros.
create or replace function public.is_profesor()
returns boolean
language sql stable security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.profiles p
    where p.id = (select auth.uid()) and p.role = 'profesor'
  );
$$;
revoke all on function public.is_profesor() from public, anon;
grant execute on function public.is_profesor() to authenticated;

create table if not exists public.convocatorias (
  id uuid primary key default gen_random_uuid(),
  nombre text not null,
  evento text not null,
  etapa text not null,
  disciplinas text[] not null,
  fecha_apertura date not null,
  fecha_cierre date not null,
  cupo_planeado integer check (cupo_planeado is null or cupo_planeado >= 0),
  publicada boolean not null default false,
  creada_por uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  constraint fechas_correctas check (fecha_cierre >= fecha_apertura),
  constraint al_menos_una_disciplina check (cardinality(disciplinas) > 0)
);

create table if not exists public.inscripciones (
  id uuid primary key default gen_random_uuid(),
  convocatoria_id uuid not null references public.convocatorias(id),
  creado_por uuid not null references auth.users(id),
  rut text not null,
  rut_normalizado text not null,
  nombre text not null,
  apellido_paterno text not null,
  apellido_materno text not null,
  fecha_nacimiento date not null,
  genero text not null check (genero in ('F','M')),
  categoria text not null check (categoria in ('SUB 10','SUB 12','SUB 14','SUB 17')),
  disciplina text not null,
  establecimiento text not null,
  comuna text not null,
  estado text not null default 'pendiente' check (estado in ('pendiente','validado')),
  created_at timestamptz not null default now(),
  constraint un_estudiante_por_disciplina unique (convocatoria_id,rut_normalizado,disciplina)
);
create index if not exists idx_inscripciones_profesor on public.inscripciones(creado_por);
create index if not exists idx_inscripciones_convocatoria on public.inscripciones(convocatoria_id);

-- Seguridad por filas. No se admiten consultas anónimas.
alter table public.profiles enable row level security;
alter table public.convocatorias enable row level security;
alter table public.inscripciones enable row level security;
revoke all on table public.profiles,public.convocatorias,public.inscripciones from anon, authenticated;
grant select on public.profiles to authenticated;
grant select,insert,update on public.convocatorias to authenticated;
grant select,insert,update on public.inscripciones to authenticated;

-- El rol es administrado exclusivamente desde Supabase (no se puede autoascender).
drop policy if exists profiles_read on public.profiles;
create policy profiles_read on public.profiles for select to authenticated
using (id = (select auth.uid()) or (select public.is_ind_admin()));

-- Convocatorias publicadas: visibles para profesores; todas para IND.
drop policy if exists convocatoria_read on public.convocatorias;
create policy convocatoria_read on public.convocatorias for select to authenticated
using (publicada or (select public.is_ind_admin()));
drop policy if exists convocatoria_insert_admin on public.convocatorias;
create policy convocatoria_insert_admin on public.convocatorias for insert to authenticated
with check ((select public.is_ind_admin()) and creada_por = (select auth.uid()));
drop policy if exists convocatoria_update_admin on public.convocatorias;
create policy convocatoria_update_admin on public.convocatorias for update to authenticated
using ((select public.is_ind_admin()))
with check ((select public.is_ind_admin()));

-- Los profesores ven solamente sus registros. IND puede ver todos.
drop policy if exists inscripciones_read on public.inscripciones;
create policy inscripciones_read on public.inscripciones for select to authenticated
using (creado_por = (select auth.uid()) or (select public.is_ind_admin()));

-- Prohibir inscripción fuera de fecha y campos de disciplina alterados, incluso
-- cuando un cliente evite la interfaz Streamlit y llame a la API directamente.
drop policy if exists inscripciones_insert_profesor on public.inscripciones;
create policy inscripciones_insert_profesor on public.inscripciones for insert to authenticated
with check (
  (select public.is_profesor())
  and creado_por = (select auth.uid())
  and estado = 'pendiente'
  and exists (
    select 1 from public.convocatorias c
    where c.id = convocatoria_id
      and c.publicada
      and ((now() at time zone 'America/Coyhaique')::date) between c.fecha_apertura and c.fecha_cierre
      and disciplina = any(c.disciplinas)
  )
);

drop policy if exists inscripciones_update_admin on public.inscripciones;
create policy inscripciones_update_admin on public.inscripciones for update to authenticated
using ((select public.is_ind_admin()))
with check ((select public.is_ind_admin()));

-- DESPUÉS de crear cuentas en Authentication > Users, insertarlas en profiles.
-- Ejemplo: reemplazar UUIDs por IDs copiados desde Auth > Users (NO publicarlos).
-- insert into public.profiles (id,display_name,role) values
-- ('UUID_DE_PROFESOR','Profesor de prueba','profesor'),
-- ('UUID_DE_IND','IND de prueba','ind');
