
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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "curso.h"
#include "sisu.h"


int main(int argc, char *argv[]) {
    int ncursos, nalunos;
    
    // info cursos
    Curso *cursos;
    // info alunos
    Aluno *alunos;
    scanf("%d %d\n", &ncursos, &nalunos);
    
    // Alocando memória para cursos e alunos
    cursos = (Curso*) malloc(ncursos * sizeof(Curso));
    alunos = (Aluno*) malloc(nalunos * sizeof(Aluno));
    
    int i = 0;
    size_t len;  // para strlen

    for(i = 0; i < ncursos; i++)
    {
        fgets(cursos[i].nome, 100, stdin);
        // Remove \n do final da string (evita erros com impressão)
        len = strlen(cursos[i].nome);
        if (len > 0 && cursos[i].nome[len - 1] == '\n')
            cursos[i].nome[len - 1] = '\0';
        scanf("%d\n", &cursos[i].vagas);
        cursos[i].aprovados = 0;
        cursos[i].notacorte = 0.0;
        cria_vazia(&cursos[i].classificados);
        cria_vazia(&cursos[i].espera);
    }

    for (i = 0; i < nalunos; i++)
    {
        fgets(alunos[i].nome, 100, stdin);
        // Remove \n do final da string (evita erros com impressão)
        len = strlen(alunos[i].nome);
        if (len > 0 && alunos[i].nome[len - 1] == '\n')
            alunos[i].nome[len - 1] = '\0';
        // Lê detalhes do aluno
        scanf("%f %d %d\n", &alunos[i].nota,
            &alunos[i].curso1, &alunos[i].curso2);
    }

    // Para cada aluno, tenta alocar o aluno em alguma de suas opções
    allocate_students(cursos, alunos, nalunos);

    // Imprime as classificacoes
    imprime_classificacoes(cursos, 0);
    for(i = 1; i < ncursos; i++)
    {
        printf("\n");
        imprime_classificacoes(cursos, i);
    }
    
}