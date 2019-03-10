# Problem przepływowy (ang. flowshop)

### Wyniki badań

[tu można dać tę tabelę ]


#### Wnioski
- Algorytm Johnsona stosowany dla dwóch maszyn pozwala na wyznaczenie optymalnej kolejności wykonywanych zadań, poprzez zminimalizowanie całkowitego czasu potrzebnego na ukończenie prac na wszystkich maszynach (*makespan*).
- Algorytm Johnsona pozwala na uzyskanie takiego samego *makespan*’u jak przegląd zupełny, jednak czas obliczeń jest znacznie krótszy, co jest widoczne szczególnie w przypadku dużej ilości zadań.
- Stosowanie algorytmu Johnsona dla trzech maszyn może być nieco kłopotliwe, ponieważ polega ono na odpowiednim podziale zadań na dwie wirtualne maszyny, wykonaniu na nich dwumaszynowego algorytmu Johnsona i zastosowaniu uzyskanej kolejności zadań na trzech maszynach. Żeby tak uzyskana kolejność była optymalna na trzech maszynach, musi wystąpić co najmniej jeden z następujących warunków:
  - czas wykonania najkrótszego zadania na maszynie nr. 1 musi być większy lub równy czasowi wykonania najdłuższego zadania na maszynie nr. 2
  - czas wykonania najkrótszego zadania na maszynie nr. 3 musi być większy lub równy czasowi wykonania najdłuższego zadania na maszynie nr. 2

