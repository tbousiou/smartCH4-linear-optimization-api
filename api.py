from typing import List, Annotated
from fastapi import Body, Query, FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from solver import solve_lp
import pandas as pd

# app = FastAPI(openapi_url='/openapi.json')
app = FastAPI(
    title="smartCH4 waste optimization API",
    description="Optimize the cost of waste for methane production using linear programming",
)

class Substrate(BaseModel):
    name: str
    methane_potential: float
    weight: float
    lipids: float
    cost_per_kg: float
    distance: int


EXAMPLES = [
    {
        "name": "S1",
        "methane_potential": 9,
        "weight": 45,
        "lipids": 0.11,
        "cost_per_kg": 2.5,
        "distance": 1
    },
    {
        "name": "S2",
        "methane_potential": 10,
        "weight": 35,
        "lipids": 0.08,
        "cost_per_kg": 2,
        "distance": 1
    }
]


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>smartCH4 Waste Optimization API</title>
        </head>
        <body>
            <h1>smartCH4 Waste Optimization API</h1>
            <p>Optimize the cost of waste for methane production using linear programming</p>
            <p>Go to <a href="docs">/docs</a> to see the API documentation.</p>
            <p><a href="https://github.com/tbousiou/smartCH4-linear-optimization-api">GitHub repository</a></p>
        </body>
    </html>
    """

@app.post("/solve")
def solve(data: Annotated[
    List[Substrate],
    Body(examples=[EXAMPLES])
], target: Annotated[int, Body(examples=[700])],
multiple_solutions: bool = Query(False, description="Whether to return multiple solutions")
):

    # def solve(data: List[Substrate]):
    # Convert each item in data to a dictionary
    data_dict = [item.model_dump() for item in data]
    # Convert the data to a DataFrame
    df = pd.DataFrame(data_dict)
    # Set 'name' as the index
    df.set_index('name', inplace=True)
    

    if multiple_solutions:
        test_target_deviations = [-10, -5, -2, 0, 2, 5, 10]
    else:
        test_target_deviations = [0]

    solutions = []
    for i in test_target_deviations:

        test_target = target + (i/100)*target

        solution = solve_lp(df, test_target)
        solutions.append(solution)

    # Call the solve_lp function with the data
    # result = solve_lp(data)
    # result = solve_lp(df, total_target=target)
    
    return solutions