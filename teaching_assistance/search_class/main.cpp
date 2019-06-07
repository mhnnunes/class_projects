
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


#include <bits/stdc++.h>

#include "Arvore.h"

using namespace std;


int main(int argc, char *argv[]) // para leitura de parâmetros
{
    // ========================= SEQUENCIAL
    Tabela T;
    Inicializa(&T);
    for (int i = 0; i < 20; i++)
    {
        Registro reg;
        reg.Chave = i;
        Insere(reg, &T);
    }
    Indice i = Sequencial((TipoChave) 5, &T);
    printf("A pesquisa na tabela retornou: %d. \
        \nEsta posição contém: %d\n", i, T.Item[i].Chave);

    // ========================= SEQUENCIAL

    // ========================= BINARIA
    Tabela T2;
    Inicializa(&T2);
    char charvector[] = {'A', 'A', 'A', 'C', 'E', 'E', 'E', 'G', 'H',
                        'I', 'L', 'M', 'N', 'P', 'R'};
    for (int i = 0; i < 15; i++)
    {
        Registro reg;
        reg.Chave = i;
        reg.character = charvector[i];
        Insere(reg, &T2);
    }
    Indice i2 = Binaria('L', &T2);
    printf("A pesquisa na tabela retornou: %d. \
        \nEsta posição contém: %c\n", i2, T2.Item[i2].character);
    // E se procurar algum elemento que repete?
    i2 = Binaria('A', &T2);
    printf("A pesquisa na tabela retornou: %d. \
        \nEsta posição contém: %c\n", i2, T2.Item[i2].character);
    // ========================= BINARIA

    // ========================= ARVORE

    TipoDicionario arvore;
    Inicializa(&arvore);

    // insere os elementos em ordem
    int arr[] = {6, 5, 8, 7, 4, 2, 3, 1, 12, 10, 9, 15};

    for (int i = 0; i <= 11; i++)
    {
        Registro reg;
        reg.Chave = arr[i];
        reg.character = 'a';
        Insere(reg, &arvore);
    }
    
    printf("realizando o caminhamento em ordem na arvore\n");
    emOrdem(arvore);
    printf("\n\n\n");

    // Pesquisa elementos na arvore
    {
        Registro reg;
        reg.Chave = 9;
        reg.character = 'b';
        printf("antes da busca: %d, %c\n", reg.Chave, reg.character);
        Pesquisa(&reg, arvore);
        printf("pesquisa retornou: %d, %c\n", reg.Chave, reg.character);

        reg.Chave = 999;
        Pesquisa(&reg, arvore);
        printf("pesquisa retornou: %d\n", reg.Chave);
    }


    // Remove elementos da Arvore
    { // Apaga o 9
        Registro reg;
        reg.Chave = 9;
        Retira(reg, &arvore);
        printf("após retirada do 9\n");
        emOrdem(arvore);
        printf("\n\n");

        reg.Chave = 4;
        Retira(reg, &arvore);
        printf("após retirada do 4\n");
        emOrdem(arvore);
        printf("\n\n");

        reg.Chave = 8;
        Retira(reg, &arvore);
        printf("após retirada do 8\n");
        emOrdem(arvore);
        printf("\n\n");


        reg.Chave = 6;
        Retira(reg, &arvore);
        printf("após retirada do 6\n");
        emOrdem(arvore);
        printf("\n\n");    
        
    }
    // ========================= ARVORE

    
    exit(0);
}