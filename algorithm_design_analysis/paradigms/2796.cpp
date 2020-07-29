
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

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'

#define MAX_DIM 1001
#define MAX_TABLES 1000010


// widths holds the largest width seen on plant for each height
int widths[MAX_DIM];

// tablewidths: Each position i holds:
//     [i][0]: largest width seen on tables (that fit in the house)
//     for each height
//     [i][1]: area (i * [i][1])
int tablewidths[MAX_DIM][2];

// tables[i][0] holds the table height
// tables[i][1] holds the table width
int tables[MAX_TABLES][3];
// House plant
int A[MAX_DIM][MAX_DIM];

// ================= Geeks for Geeks code
void update_width(int i, int width){
    if(widths[i] < width) widths[i] = width;
}

// Finds the maximum area under the histogram represented 
// by histogram.  See below article for details. 
// https://www.geeksforgeeks.org/largest-rectangle-under-histogram/ 
int maxHist(int row[], int C) 
{ 
    // Create an empty stack. The stack holds indexes of 
    // hist[] array/ The bars stored in stack are always 
    // in increasing order of their heights. 
    stack<int> result; 
  
    int top_val;     // Top of stack
    int max_area = 0; // Initialize max area in current 
                      // row (or histogram) 
    int width = 0;
    int area = 0;    // Initialize area with current top 
  
    // Run through all bars of given histogram (or row) 
    int i = 0; 
    while (i < C) 
    { 
        // If this bar is higher than the bar on top stack, 
        // push it to stack 
        if (result.empty() || row[result.top()] <= row[i]) 
            result.push(i++); 
  
        else
        { 
            // If this bar is lower than top of stack, then 
            // calculate area of rectangle with stack top as 
            // the smallest (or minimum height) bar. 'i' is 
            // 'right index' for the top and element before 
            // top in stack is 'left index' 
            top_val = row[result.top()]; 
            result.pop(); 
            // area = top_val * i; 

            width = (result.empty())? i : i - result.top() - 1;
            update_width(top_val, width);
            area = top_val * width;

            max_area = max(area, max_area); 
        } 
    } 
  
    // Now pop the remaining bars from stack and calculate area 
    // with every popped bar as the smallest bar 
    while (!result.empty()) 
    { 
        top_val = row[result.top()]; 
        result.pop(); 
        width = (result.empty())? i : i - result.top() - 1;
        update_width(top_val, width);
        area = top_val * width;
  
        max_area = max(area, max_area); 
    } 
    return max_area; 
} 
  
// Returns area of the largest rectangle with all 1s in A[][] 
int maxRectangle(int R, int C) 
{ 
    // Calculate area for first row and initialize it as 
    // result 
    int result = maxHist(A[0], C); 
  
    // iterate over row to find maximum rectangular area 
    // considering each row as histogram 
    for (int i = 1; i < R; i++) 
    { 
  
        for (int j = 0; j < C; j++) 
  
            // if A[i][j] is 1 then add A[i -1][j] 
            if (A[i][j]) A[i][j] += A[i - 1][j]; 
  
  
        // Update result if area with current row (as last row) 
        // of rectangle) is more 
        result = max(result, maxHist(A[i], C)); 
    } 
  
    return result; 
} 

// ============= GFG

int main(){ _
    char aux;
    int n, m;
    int ntables;
    int area;

    scanf("%d", &n);
    scanf("%d", &m);

    // Read available positions
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            scanf(" %c", &aux);
            A[i][j] = (aux == '.');
        }
    }

    // Read tables' sizes
    scanf("%d", &ntables);
    
    memset(widths, -1, MAX_DIM * sizeof(int));
    for (int i = 0; i < ntables; i++)
    {
        scanf("%d", &tables[i][0]);
        scanf("%d", &tables[i][1]);
        area = tables[i][0] * tables[i][1];
        tables[i][2] = area;
    }

    int largestrec = maxRectangle(n, m);

    memset(tablewidths, -1, 2 * MAX_DIM * sizeof(int));
    for(int i = 0; i < ntables; i++)
    {
        // tables[i][0] may be width or height
        if(widths[tables[i][0]] >= tables[i][1] ||
           widths[tables[i][1]] >= tables[i][0]) // table fits
        {
            if(tables[i][2] > tablewidths[tables[i][0]][1])
            {
                tablewidths[tables[i][0]][1] = tables[i][2];
                tablewidths[tables[i][0]][0] = tables[i][1];
            }
        }
    }

    int maxareai = 0;
    int maxarea = 0;
    for (int i = 0; i <= min(500, max(n, m)); i++)
    {
        if(tablewidths[i][1] > maxarea)
        {
            maxareai = i;
            maxarea = tablewidths[i][1];
        }else if(tablewidths[i][1] == maxarea && tablewidths[i][0] > tablewidths[maxareai][0])
        {
            maxareai = i;
            maxarea = tablewidths[i][1];
        }
    }

    printf("%d %d\n", maxareai, tablewidths[maxareai][0]);
    exit(0);
}


