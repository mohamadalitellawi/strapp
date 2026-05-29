# Step 0 — What we are building

Welcome! This guide teaches you two things at the same time:

1. How to build a small **web app** with a tool called **Streamlit**.
2. How **structural load combinations** work (the American code, ASCE 7-22).

You do **not** need to be an expert. We explain every step in simple words.

## Who is this for?

- **Junior Python developers** who want to build their first real web app.
- **Structural engineers** who want to learn a little Python and automation.

If you have never written Python before, that is fine. Take it slowly and copy
the steps one at a time.

## What is the app?

A web page with three tabs:

- **Calculator tab.** You type in your building loads (like the weight of the
  floor, the people, the snow, the wind). The app mixes them using code rules
  and tells you the **worst combination** — the one your design must survive.

- **Simulation tab.** Real loads are never exact. So the app rolls the dice many
  times, trying many possible load values, and shows you the worst case out of
  all of them. This is a simple version of a "Monte Carlo" study.

- **About tab.** A short note on what the app teaches and which library versions
  it is running.

## What is a "load combination"? (very short version)

A building feels many loads at once: its own weight, people, furniture, snow,
wind, earthquakes. These do not all reach their maximum at the same moment. The
code gives us **recipes** that mix the loads in safe ways. For example:

```
1.2 × (dead load) + 1.6 × (live load)
```

We must check every recipe and design for the biggest result. Step 2 explains
this properly.

## The tools we use

| Tool | What it is for |
| ---- | -------------- |
| **uv** | Sets up the project and installs libraries. Very fast. |
| **ruff** | Checks and tidies our code style. |
| **ty** | Checks our types (it is new and still in preview). |
| **pytest** | Runs automatic tests. |
| **Streamlit** | Turns Python into a web page. |
| **NumPy / pandas** | Numbers and tables. |
| **Plotly / matplotlib** | Charts. |
| **handcalcs** | Shows math the way an engineer writes it by hand. |

## The plan

We will go through these guides in order:

1. **Set up the project** with uv.
2. **Understand load combinations.**
3. **Build the Streamlit app.**
4. **Add quality checks**: ruff, ty, and tests.
5. **Build and publish** the package.
6. **Push to GitHub.**
7. **Put the app online** for free.

Ready? Go to [Step 1](01_setup_uv_project.md).
