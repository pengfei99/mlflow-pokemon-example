echo "Predict five noraml pokemon:";
curl -X POST -H "Content-Type:application/json; format=pandas-split" --data \
'{"columns":["hp","attack","defense","special_attack","special_defense","speed"],"index":[272,293,414,263,49],
"data":[[80,70,70,90,100,70],[64,51,23,51,23,28],[70,94,50,94,50,66],[38,30,41,30,41,60],[70,65,60,90,75,90]]}' \
http://127.0.0.1:8001/invocations ;


echo "Predict five legendary pokemon:";
curl -X POST -H "Content-Type:application/json; format=pandas-split" --data \
'{"columns":["hp","attack","defense","special_attack","special_defense","speed"],"index":[384,150,482,382,485],
"data":[[105,180,100,180,100,115],[106,150,70,194,120,140],[75,125,70,125,70,115],[100,150,90,180,160,90],[91,90,106,130,106,77]]}' \
http://127.0.0.1:8001/invocations ;