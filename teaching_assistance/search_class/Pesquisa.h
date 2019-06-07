
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

#ifndef PESQUISA_H
#define PESQUISA_H

#include <iostream>

# define MAX 1000

typedef int TipoChave;

typedef struct {
    TipoChave Chave;
    char character;
	/* outros componentes */
} Registro;

typedef int Indice;

typedef struct {
    Registro Item[MAX + 1];
    Indice n;
} Tabela;

void Inicializa(Tabela *T);
Indice Sequencial(TipoChave x, Tabela *T);
void Insere(Registro Reg, Tabela *T) ;
void Remove(TipoChave x, Tabela *T) ;
Indice Binaria(char x, Tabela *T) ;

#endif