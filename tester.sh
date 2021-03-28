#!/bin/bash

runner=$1

if test -f Main.py
then
	runner="python3.7 Main.py"
elif test -f Main.java
then
	echo "Attempting to compile..."
	javac *.java
	runner="java Main"
fi

score=0
error=0

for value in {0..9}
do
	echo ""
	echo "Running ${value}.code"
	timeout 5 ${runner} Correct/${value}.code Correct/${value}.data > Correct/${value}.student
	echo "Running diff with ${value}.expected"
	if cmp -s "Correct/${value}.expected" "Correct/${value}.student"; then
		echo "Print looks good"
		score=$(($score + 1))
	else
		echo "Student output and expected output are different"
	fi
done

echo ""
echo "Running error cases:"
echo ""

echo "Running 00.error:"
timeout 5 ${runner} Error/00.code Error/00.data
read -n 1 -p "Error is new keyword used in inappropriate location. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""

echo "Running 01.error:"
timeout 5 ${runner} Error/01.code Error/01.data
read -n 1 -p "Error reference variable declared in declaration sequence. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi

echo "Done!"