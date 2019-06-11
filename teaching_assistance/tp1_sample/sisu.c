
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
#include "sisu.h"


void move_primeiro_para_espera(Curso *cursos, float *notacorte, int cursoatual)
{
	NoAlunoPointer primeiro = remove_primeiro(&cursos[cursoatual].classificados);
	if(primeiro != NULL) {
		// Move o primeiro pra lista de espera da primeira opção
		// reaproveitando a celula
    	insere_ordenado(&cursos[primeiro->aluno->curso1].espera,
    		primeiro, notacorte, primeiro->aluno->curso1);
    	// Cria outra celula com o primeiro e coloca na lista de
    	// espera da segunda opção
		cria_e_insere_ordenado(&cursos[primeiro->aluno->curso2].espera,
				primeiro->aluno, primeiro->aluno->curso2);
    }
}

void allocate_students(Curso *cursos, Aluno *alunos, int nalunos){
	int i = 0;
	NoAlunoPointer p;
	float notacorte = 0.0;
	int cursoatual;

	for (i = 0; i < nalunos; ++i)
	{
		// tenta alocar aluno no curso
		if(cursos[alunos[i].curso1].aprovados < cursos[alunos[i].curso1].vagas)
		{ // tem vaga na primeira opção
			// curso atual é a primeira op do aluno
			cursoatual = alunos[i].curso1;
			notacorte = \
				cria_e_insere_ordenado(&cursos[cursoatual].classificados,
					&alunos[i], cursoatual);
			cursos[cursoatual].aprovados++;
			if (notacorte > cursos[cursoatual].notacorte &&
				cursos[cursoatual].vagas == cursos[cursoatual].aprovados)

			{
				cursos[cursoatual].notacorte = notacorte;
			}
		}else if(cursos[alunos[i].curso2].aprovados <
			cursos[alunos[i].curso2].vagas)
		{ // tem vaga na segunda opção
			// curso atual é a primeira op do aluno
			cursoatual = alunos[i].curso2;
			notacorte = \
				cria_e_insere_ordenado(&cursos[cursoatual].classificados,
					&alunos[i], cursoatual);
			cursos[cursoatual].aprovados++;
			if (notacorte > cursos[cursoatual].notacorte &&
				cursos[cursoatual].vagas == cursos[cursoatual].aprovados)
			{
				cursos[cursoatual].notacorte = notacorte;
			}
			// insere aluno na espera da primeira anyway (regra)
			cria_e_insere_ordenado(&cursos[alunos[i].curso1].espera,
			&alunos[i], alunos[i].curso1);
		}
		else
		{
			// tenta achar uma vaga na primeira opção
			// curso atual é a primeira op do aluno
			cursoatual = alunos[i].curso1;
			p = NULL;
			p = encontra_posicao(&cursos[cursoatual].classificados,
				&alunos[i], cursoatual);
			if(p != cursos[cursoatual].classificados.first)
			{  // achou vaga na primeira opção
				move_primeiro_para_espera(cursos, &notacorte, cursoatual);
				notacorte = \
					cria_e_insere_ordenado(&cursos[cursoatual].classificados,
						&alunos[i], cursoatual);
				if (notacorte > cursos[cursoatual].notacorte)
					cursos[cursoatual].notacorte = notacorte;
			}
			else // tenta achar uma vaga na segunda opção
			{
				 // curso atual é a segunda op do aluno
				cursoatual = alunos[i].curso2;
				p = encontra_posicao(&cursos[cursoatual].classificados,
				&alunos[i], cursoatual);
				if(p != cursos[cursoatual].classificados.first)
				{  // achou vaga na segunda opção
					move_primeiro_para_espera(cursos, &notacorte, cursoatual);
					notacorte = \
						cria_e_insere_ordenado(&cursos[cursoatual].classificados,
							&alunos[i], cursoatual);
					if (notacorte > cursos[cursoatual].notacorte)
						cursos[cursoatual].notacorte = notacorte;
					// insere aluno na espera da primeira anyway (regra)
					cria_e_insere_ordenado(&cursos[alunos[i].curso1].espera,
					&alunos[i], alunos[i].curso1);
				}else
				{ // insere o aluno nas duas listas de espera
					cria_e_insere_ordenado(&cursos[alunos[i].curso1].espera,
					&alunos[i], alunos[i].curso1);
					cria_e_insere_ordenado(&cursos[alunos[i].curso2].espera,
						&alunos[i], alunos[i].curso2);
				}
			}
		}
	}
}

