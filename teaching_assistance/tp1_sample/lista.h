
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

#ifndef LISTA_H
#define LISTA_H

#include <stdio.h>
#include <stdlib.h>

#include "aluno.h"


typedef struct NoAluno *NoAlunoPointer;
typedef struct NoAluno
{
    Aluno* aluno;
    NoAlunoPointer next; // Ponteiro para o próximo elemento
    NoAlunoPointer prev; // Ponteiro para o elemento anterior
}NoAluno;

typedef struct ListaAluno
{
    NoAluno *first; // Ponteiro para o primeiro elemento
    NoAluno *last; // Ponteiro para o último elemento
}ListaAluno;

// Confere se a lista está vazia
int vazia(ListaAluno Lista);
// Cria lista vazia
void cria_vazia(ListaAluno *Lista);
// Remove o primeiro elemento da lista, e o retorna
NoAlunoPointer remove_primeiro(ListaAluno *Lista);
// Cria uma célula e insere-a na lista de maneira ordenada
float cria_e_insere_ordenado(ListaAluno *Lista, Aluno *a,
    int cursoatual);
// Insere uma célula na lista de maneira ordenada
void insere_ordenado(ListaAluno *Lista, NoAlunoPointer nap, float *notacorte,
    int cursoatual);
// Encontra a posição ideal para o aluno na lista
NoAlunoPointer encontra_posicao(ListaAluno *Lista, Aluno *a, int cursoatual);


#endif