#!/bin/bash
touch result_amazon.csv
{ echo "id";  } | tr "\n" " " > result_amazon.csv
cut -d, -f1,2,4,6,8,10,12,14 result.csv >> result_amazon.csv