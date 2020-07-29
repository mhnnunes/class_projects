
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
 * Problem: Lucro
 * Link: https://www.urionlinejudge.com.br/judge/pt/problems/view/1310
 */


#include <bits/stdc++.h>
#define _ ios_base::sync_with_stdio(0);cin.tie(0);

using namespace std;

typedef long long ll;
typedef pair<int, int> ii;

const int INF = 0x3f3f3f3f;

int income[60];

int mss(int n) 
{
    int sum_without_suffix = -INF;
    int sum_with_suffix = 0; 
  
    for (int i = 0; i < n; i++)
    {
        sum_with_suffix = sum_with_suffix + income[i];
        sum_without_suffix = max(sum_without_suffix, sum_with_suffix);
        sum_with_suffix = max(sum_with_suffix, 0);
    }
    return sum_without_suffix;
} 

int main()
{ _
    int ndays;
    int costperday;    

    while(scanf("%d", &ndays) != EOF){
        scanf("%d", &costperday);
        for(int i = 0; i < ndays; i++)
        {
            scanf("%d", &income[i]);
            income[i] -= costperday;
        }

        printf("%d\n", max(0, mss(ndays)));
    }
    exit(0);
}