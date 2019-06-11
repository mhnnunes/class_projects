
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

#include "curso.h"


void imprime_classificacoes(Curso *cursos, int i)
{
    printf("%s %.2f\n", cursos[i].nome, cursos[i].notacorte);
    printf("Classificados\n");
    NoAlunoPointer p;
    p = cursos[i].classificados.last;
    while(p != cursos[i].classificados.first || p->aluno != NULL){
        printf("%s %.2f\n", p->aluno->nome, p->aluno->nota);
        p = p->prev;
    }
    printf("Lista de espera\n");
    p = cursos[i].espera.last;
    while(p != cursos[i].espera.first || p->aluno != NULL){
        printf("%s %.2f\n", p->aluno->nome, p->aluno->nota);
        p = p->prev;
    }
}
