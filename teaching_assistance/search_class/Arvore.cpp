
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


#include "Arvore.h"

void Inicializa(Apontador *Dicionario) {
    *Dicionario = NULL;
}

void Pesquisa(Registro *x, Apontador p) {
    if (p == NULL)
    {
        printf("Registro nao esta presente \n");
        x->Chave = -1;
    }
    else if (x->Chave < p->Reg.Chave)
        Pesquisa(x, p->Esq);
    else if (x->Chave > p->Reg.Chave)
        Pesquisa(x, p->Dir);
    else
        *x = p->Reg;
}

void Insere(Registro x, Apontador *p) {
    if (*p == NULL) {
        *p = (Apontador) malloc (sizeof(No));
        (*p)->Reg = x;
        (*p)->Esq = NULL;
        (*p)->Dir = NULL;
    }
    else if (x.Chave < (*p)->Reg.Chave)
        Insere(x, &(*p)->Esq);
    else if (x.Chave > (*p)->Reg.Chave)
        Insere(x, &(*p)->Dir);
    else
        printf("Registro ja existe na arvore\n");
}

void Retira(Registro x, Apontador *p) {
    Apontador Aux;
    if (*p == NULL) {
        printf("Registro nao esta na arvore\n");
    }
    else if (x.Chave < (*p)->Reg.Chave) {
        Retira(x, &(*p)->Esq);
    }
    else if (x.Chave > (*p)->Reg.Chave){
        Retira(x, &(*p)->Dir);
    }
    else if ((*p)->Dir == NULL) {
        Aux = *p;
        *p = (*p)->Esq;
        free(Aux);
    }
    else if ((*p)->Esq == NULL) {
        Aux = *p;
        *p = (*p)->Dir;
        free(Aux);
    }
    else
        // Antecessor(*p, &(*p)->Esq);
        Sucessor(*p, &(*p)->Dir);
}

void Sucessor(Apontador q, Apontador *r) {
    printf("Entrou na sucessor %d\n", (*r)->Reg.Chave);
    if((*r)->Esq != NULL) {
        Sucessor(q, &(*r)->Esq);
        return;
    }
    q->Reg = (*r)->Reg;
    q = *r;
    *r = (*r)->Dir;
    free(q);
}

void Antecessor(Apontador q, Apontador *r) {
    if ( (*r)->Dir != NULL) {
        Antecessor(q, &(*r)->Dir);
        return;
    }
    q->Reg = (*r)->Reg;
    q = *r;
    *r = (*r)->Esq;
    free(q);
}

void preOrdem(Apontador no) {
    if (no != NULL) {
        printf("%d ",no->Reg.Chave);
        preOrdem(no->Esq);
        preOrdem(no->Dir);
    }
}

void emOrdem(Apontador no) {
    if(no != NULL) {
        emOrdem(no->Esq);
        printf("%d ",no->Reg.Chave);
        emOrdem(no->Dir);
    }
}

void posOrdem(Apontador no)
{
    if (no != NULL) {
        posOrdem(no->Esq);
        posOrdem(no->Dir);
        printf("%d ",no->Reg.Chave);
    }
}