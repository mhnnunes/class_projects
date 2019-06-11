
// Copyright 2019 Matheus Nunes <mhnnunes@dcc.ufmg.br>
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

#ifndef SISU_H
#define SISU_H

// Move o primeiro aluno do curso para a lista de espera
// (quando o aluno é desqualificado pela entrada de outro)
void move_primeiro_para_espera(Curso *cursos, float *notacorte,
    int cursoatual);
// Aloca todos os alunos no curso (função principal do programa)
void allocate_students(Curso *cursos, Aluno *alunos, int nalunos);

#endif
