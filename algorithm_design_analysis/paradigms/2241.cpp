
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

/*
 * Author: Matheus Henrique do Nascimento Nunes
 * Problem: GO--
 * Link: https://www.urionlinejudge.com.br/judge/pt/problems/view/2241
 */


#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'

#define MAX_BOARD_SIZE 510

int black_board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
int white_board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];

int ans_white, ans_black;

void buildDP(int n){
    for(int k = 1; k < n; k++) // sub_matrix size
    {
        for (int i = 1; i <= n - k; i++)
        {
            for (int j = 1; j <= n - k; j++)
            {
                //check white and black matrices
                if(black_board[i][j] != -1 && black_board[i][j+1] != -1 &&
                   black_board[i+1][j] != -1 && black_board[i+1][j+1] != -1)
                {
                    if(black_board[i][j] == 1 || black_board[i][j+1] == 1 ||
                       black_board[i+1][j] == 1 || black_board[i+1][j+1] == 1)
                    {
                        ans_black++;
                        black_board[i][j] = 1;
                    }
                }
                else
                {
                    black_board[i][j] = -1;
                }
                
                if(white_board[i][j] != -1 && white_board[i][j+1] != -1 &&
                   white_board[i+1][j] != -1 && white_board[i+1][j+1] != -1)
                {
                    if(white_board[i][j] == 1 || white_board[i][j+1] == 1 ||
                       white_board[i+1][j] == 1 || white_board[i+1][j+1] == 1)
                    {
                        ans_white++;
                        white_board[i][j] = 1;
                    }
                }
                else
                {
                    white_board[i][j] = -1;
                }
            }
        }
    }
}

int main(){ _
    int board_size, pieces;
    int x, y;
    scanf("%d", &board_size);
    scanf("%d", &pieces);

    // initialize DPs with neutral value, 0
    memset(white_board, 0, sizeof(int) * MAX_BOARD_SIZE * MAX_BOARD_SIZE);
    memset(black_board, 0, sizeof(int) * MAX_BOARD_SIZE * MAX_BOARD_SIZE);
    ans_black = 0;
    ans_white = 0;
    
    // black pieces
    for (int i = 0; i < pieces; i++)
    {
        scanf("%d", &x);
        scanf("%d", &y);
        white_board[x][y] = -1;
        black_board[x][y] = 1; // black piece is positive on black DP
        ans_black++; // mark pieces as sub-matrix 1x1
    }

    // white pieces
    for (int i = 0; i < pieces; i++)
    {
        scanf("%d", &x);
        scanf("%d", &y);
        white_board[x][y] = 1; // white piece is positive on black DP
        black_board[x][y] = -1;
        ans_white++; // mark pieces as sub-matrix 1x1
    }
    buildDP(board_size);
    printf("%d %d\n", ans_black, ans_white);
    exit(0);

}


