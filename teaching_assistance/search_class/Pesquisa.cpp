
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


#include "Pesquisa.h"

void Inicializa(Tabela *T) {
    T->n = 0;
}

// ==================================================== SEQUENCIAL: INICIO

/* retorna 0 se não encontrar um registro com a chave x */
Indice Sequencial(TipoChave x, Tabela *T){
    int i;
    T->Item[0].Chave = x; /* sentinela */
    i = T->n + 1;
    do {
        i--;
    } while (T->Item[i].Chave != x);
    return i;
}

void Insere(Registro Reg, Tabela *T) {
    if (MAX == T->n)
        printf("Erro : tabela cheia\n");
    else {
        T->n++;
        T->Item[T->n] = Reg;
    }
}

void Remove(TipoChave x, Tabela *T) {
    int idx;
    idx = Sequencial(x, T);
    /* se encontrou o item, troca pelo último, reduz o n */
    if (idx != 0) T->Item[idx] = T->Item[T->n--];
}

// ==================================================== SEQUENCIAL: FIM

// ==================================================== BINARIA: INICIO

Indice Binaria(char x, Tabela *T) {
    printf("Iniciando a busca binaria\n");
    Indice meio, Esq, Dir;
    if (0 == T->n) return 0; /* vetor vazio */
    Esq = 1;
    Dir = T->n;
    do {
        meio = (Esq + Dir) / 2;
        if (x > T->Item[meio].character)
        {
            Esq = meio + 1; /* procura na partição direita */
            printf("Novo inicio: %d\n", Esq);
        }
        else
        {
            Dir = meio - 1; /* procura na partição esquerda */
            printf("Novo fim: %d\n", Dir);
        }
    } while ((x != T->Item[meio].character) && (Esq <= Dir));
    if (x == T->Item[meio].character)
        return meio;
    else
        return 0;
}

// ==================================================== BINARIA: FIM