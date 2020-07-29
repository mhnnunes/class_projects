
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
 * Problem: Ginástica
 * Link: https://www.urionlinejudge.com.br/judge/pt/problems/view/2664
 */

#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'

typedef unsigned long long ull;
typedef unsigned int ui;

#define MAX_MINUTES 55
#define MAX_INTERVAL 100010
#define MOD_VALUE (((int) 1e9 ) + 7)

ull DP[MAX_MINUTES][MAX_INTERVAL];
int MAX_COL;

ull calculateBottomUp(int minutes, int interval_end)
{
	ull result = 0LL;
	
	for(int i = 0; i <= interval_end; i++)
		DP[0][i] = 1;

	for(int i = 1; i < minutes; i++)
	{
		for(int j = 0; j <= interval_end; j++)
		{
			// Calculate DP value
			if(j == 0) DP[i][j] = (DP[i-1][j+1] % MOD_VALUE);
			else if(j == interval_end) DP[i][j] = (DP[i-1][j-1] % MOD_VALUE);
			else DP[i][j] = (DP[i-1][j-1] + DP[i-1][j+1] % MOD_VALUE);
			// Sum to result
			if(i == minutes-1)
			{
				result += (DP[i][j] % MOD_VALUE);
				result = (result % MOD_VALUE);
			}
		}
	}
	return result;
}


int main()
{ _
	int minutes, interval_start, interval_end;
	scanf("%d", &minutes);
	scanf("%d", &interval_start);
	scanf("%d", &interval_end);

	// Shift interval to 0 based
	interval_end -= interval_start;
	interval_start -= interval_start;
	MAX_COL = interval_end;

	// Initialize DP
	memset(DP, -1, sizeof(ull) * MAX_MINUTES * MAX_INTERVAL);

	// Calculate DP from rows 0 to minutes-1 and columns from 0 to interval_end
	ull sum = 0LL;
	sum = calculateBottomUp(minutes, interval_end);
	printf("%llu\n", sum);
    exit(0);
}


