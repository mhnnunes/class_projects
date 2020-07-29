
# Copyright 2019 Matheus Nunes <mhnnunes@dcc.ufmg.br>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!/bin/bash

if [ ! -d "myout" ]; then
  mkdir myout
fi

echo "" > myout/out.time
echo "" > myout/out.memory

for infile in `ls -v in`; do
	# echo $infile
	echo $infile >> myout/out.memory
  echo $infile >> myout/out.time

	infile=${infile//\.in/}
	{ time ./executar.sh in/$infile.in myout/$infile.out; } 2>> myout/out.time
  #{ valgrind ./tp1 < in/$infile.in > myout/$infile.out; } 2>> myout/out.memory
	echo "" >> myout/out.memory
  echo "" >> myout/out.time

	sha1sum myout/$infile.out
done




