# Step 2 — Understand load combinations

This step explains the engineering idea. No code yet — just the thinking. Take
your time; once this clicks, the code is easy.

> ⚠️ Remember: this is for **learning**. The real code book (ASCE 7-22) has more
> rules and special cases. Never design a real building from this guide.

## 2.1 What is a "load"?

A load is anything that pushes, pulls, or weighs on a building. We give each
kind of load a short letter:

| Letter | Name | Example |
| ------ | ---- | ------- |
| `D` | Dead | The weight of the building itself (concrete, steel). |
| `L` | Live | People, furniture, movable things. |
| `Lr` | Roof Live | Workers and tools on the roof during repairs. |
| `S` | Snow | Snow sitting on the roof. |
| `R` | Rain | Rain water pooling on the roof. |
| `W` | Wind | Wind pushing on the walls and roof. |
| `E` | Seismic | Shaking from an earthquake. |

## 2.2 Why "combinations"?

All these loads can happen, but **not all at full strength at the same time**.
A huge snow storm and a huge earthquake at the same exact second is very
unlikely. So the code gives us a set of **recipes**. Each recipe says how much of
each load to add together. We then design for the **worst** recipe.

A recipe looks like this:

```
1.2D + 1.6L + 0.5S
```

This means: take 1.2 times the dead load, plus 1.6 times the live load, plus 0.5
times the snow load. The numbers (1.2, 1.6, 0.5) are called **load factors**.

## 2.3 Two design methods: LRFD and ASD

The American code gives **two** families of recipes. They are two different ways
of thinking about safety.

- **LRFD** (Load and Resistance Factor Design). Uses **big** factors like 1.2
  and 1.6. The idea: make the loads bigger on purpose to add safety, then
  compare with the full strength of the material.

- **ASD** (Allowable Stress Design). Uses factors **close to 1.0**. The idea:
  keep loads near their real size, but only allow the material to be stressed to
  a safe fraction of its strength.

Both are valid. Engineers pick one. Our app can show LRFD, ASD, or both.

## 2.4 The LRFD recipes (ASCE 7-22, Section 2.3.1)

```
1.   1.4D
2.   1.2D + 1.6L + 0.5(Lr or S or R)
3.   1.2D + 1.6(Lr or S or R) + (1.0L or 0.5W)
4.   1.2D + 1.0W + 1.0L + 0.5(Lr or S or R)
5.   1.2D + 1.0E + 1.0L + 0.2S
6.   0.9D + 1.0W
7.   0.9D + 1.0E
```

## 2.5 The ASD recipes (ASCE 7-22, Sections 2.4.1 and 2.4.5)

```
1.   D
2.   D + L
3.   D + (Lr or S or R)
4.   D + 0.75L + 0.75(Lr or S or R)
5.   D + 0.6W
6.   D + 0.75L + 0.75(0.6W) + 0.75(Lr or S or R)
7.   0.6D + 0.6W
8.   1.0D + 0.7E
9.   1.0D + 0.525E + 0.75L + 0.75S
10.  0.6D + 0.7E
```

## 2.6 What does "(Lr or S or R)" mean?

It means: pick **one** of those three (whichever is biggest for your building),
not all three. In our code we make a **separate recipe for each choice**, so you
can see every case clearly. That is why the app shows names like
`LRFD 2 (Lr)`, `LRFD 2 (S)`, and `LRFD 2 (R)`.

## 2.7 Which one "controls"?

After we work out every recipe, the one with the **biggest total** is the one
that **controls the design**. That is the number the structure must be strong
enough to carry. Our app finds it for you and highlights it in red.

## 2.8 Why the `0.9D` and `0.6D` recipes?

Look at recipe `0.9D + 1.0W`. Here the dead load is made **smaller** (0.9), not
bigger. Why? Because for a light roof, strong wind can try to **lift** the
building, like a kite. The dead weight is what holds it down. So we check the
case where the wind is strong but the helpful dead weight is a little less than
expected. This is a great example of "the worst case is not always the biggest
numbers everywhere."

## You are done with Step 2

You now understand the engineering. Next we turn these recipes into code and a
web page: [Step 3 — Build the Streamlit app](03_building_the_streamlit_app.md).
