
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
 * Problem: Six Flags
 * Link: https://www.urionlinejudge.com.br/judge/pt/problems/view/1487
 */

#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'

int play_time[110];   // weight
int play_points[110]; // value

int unboundedKnapsack(int total_time, int natractions, vector<int> &dp) 
{
    for (int i = 0; i <= total_time; i++)
    {
        for (int j = 0; j < natractions; j++)
        {
            if (play_time[j] <= i)
            {
                dp[i] = max(dp[i], dp[i - play_time[j]] + play_points[j]);
            }
        }
    }
    return dp[total_time]; 
} 

int main(){ _
    int natractions, time;
    cin >> natractions >> time;

    int inst = 1; // instance counter
    while(natractions > 0 && time > 0)
    {
        vector<int> DP(time + 10, 0);
        DP[0] = 0; // Base case: weight == 0
        for (int i = 0; i < natractions; i++)
        {
            cin >> play_time[i] >> play_points[i];
        }
        cout << "Instancia " << inst++ << endl;
        cout << unboundedKnapsack(time, natractions, DP) << endl << endl;
        cin >> natractions >> time;
    }
    exit(0);
}

