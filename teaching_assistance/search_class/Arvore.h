
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


#ifndef ARVORE_H
#define ARVORE_H

#include<iostream>
#include "Pesquisa.h"


typedef int TipoChave;


typedef struct No * Apontador;

typedef struct No {
    Registro Reg;
    Apontador Esq, Dir;
} No;

typedef Apontador TipoDicionario;

void preOrdem(Apontador no);
void emOrdem(Apontador no);
void posOrdem(Apontador no);
void Inicializa(Apontador *Dicionario);
void Pesquisa(Registro *x, Apontador p);
void Insere(Registro x, Apontador *p);
void Retira(Registro x, Apontador *p);
void Antecessor(Apontador q, Apontador *r);
void Sucessor(Apontador q, Apontador *r);


#endif