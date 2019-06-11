
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

#include "lista.h"

void cria_vazia(ListaAluno *Lista)
{ 
    // Cria uma lista duplamente encadeada, vazia
    // Lista->first é a célula cabeça
    Lista->first = (NoAlunoPointer) malloc(sizeof(NoAluno));
    Lista->last = Lista->first;
    Lista->first->next = NULL;
    Lista->first->prev = NULL;
}

int vazia(ListaAluno Lista)
{
    return (Lista.first == Lista.last);
}

NoAlunoPointer encontra_posicao(ListaAluno *Lista, Aluno *a, int cursoatual)
{
    NoAlunoPointer p = Lista->first;
    while(p->next != NULL)
    {
        if(p->next->aluno->nota > a->nota)
        {
            // O aluno da frente sempre tem a maior nota
            // A lista estará ordenada ao contrário: o primeiro aluno da lista
            // é o que possui a menor nota do curso
            break;
        }
        if(p->next->aluno->nota == a->nota){  // desempate
            if((a->curso1 == cursoatual) &&
               (p->next->aluno->curso1 == cursoatual))
            {
                // As notas dos alunos são iguais e o curso atual
                // é a primeira op dos dois: preferencia por chegada,
                // o que já está na lista vem primeiro
                break;
            }
            else if(((a->curso2 == cursoatual) &&
                      (p->next->aluno->curso1 == cursoatual)) ||
                     ((a->curso2 == cursoatual) &&
                       (p->next->aluno->curso2 == cursoatual))
                     )
            {
                break;
                // As notas sao iguais e o curso atual é a segunda op do que
                // está entrando e primeira op do que já está na lista
                // (preferencia por primeira opção)
            }
        }       
        p = p->next;
    }
    return p;
    // p vai ser ou Lista->first (celula cabeça) ou posição após a qual
    // o aluno deve ser inserido
}

float cria_e_insere_ordenado(ListaAluno *Lista, Aluno *a, int cursoatual)
{
    // Cria célula para o Aluno e insere a célula de maneira ordenada
    // na lista
    float notacorte = 0.0;
    NoAlunoPointer node = (NoAlunoPointer) malloc(sizeof(NoAluno));
    node->aluno = a;
    insere_ordenado(Lista, node, &notacorte, cursoatual);
    return notacorte;
}


void insere_ordenado(ListaAluno *Lista, NoAlunoPointer nap, float *notacorte,
    int cursoatual)
{
    // Insere a célula do Aluno de maneira ordenada na lista
    NoAlunoPointer p = Lista->first;
    p = encontra_posicao(Lista, nap->aluno, cursoatual);
    if(p == Lista->first){
        // Atualiza a nota de corte se o aluno é o primeiro
        // da lista (aluno com a menor nota)
        *notacorte = nap->aluno->nota;
    }else{
        // Atualiza a nota de corte sempre, utilizando a nota do primeiro
        // aluno do curso (aluno com menor nota)
        if(Lista->first->next != NULL && Lista->first->next->aluno != NULL)
            *notacorte = Lista->first->next->aluno->nota;
    }
    nap->next = p->next;
    if (p->next != NULL) p->next->prev = nap;
    p->next = nap;
    nap->prev = p;
    if(p == Lista->last){
        Lista->last = nap;
    }
}

NoAlunoPointer remove_primeiro(ListaAluno *Lista)
{
    NoAlunoPointer p  = Lista->first;
    NoAlunoPointer q;
    if(vazia(*Lista) || p == NULL || p->next == NULL)
    {
        // Erro: Lista vazia ou posição não existe
        return NULL;
    }
    q = p->next; // estou removendo q
    p->next = q->next;
    if(q->next != NULL) q->next->prev = p;
    if (p->next == NULL) Lista->last= p;
    return q;
}
