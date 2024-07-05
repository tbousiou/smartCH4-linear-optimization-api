from typing import List, Annotated
from fastapi import Body, Query, FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from solver import solve_lp
import pandas as pd

# app = FastAPI(openapi_url='/openapi.json')
app = FastAPI(
    title="smartCH4 Biogas Waste Optimization API",
    description="Optimize the cost of waste for biogas production using linear programming",
)

class Substrate(BaseModel):
    name: str
    Biogas: float
    Weight: float
    Fat: float
    Cost: float
    Distance: int


EXAMPLES = [
    {
        "name": "S1",
        "Biogas": 9,
        "Weight": 60,
        "Fat": 0.11,
        "Cost": 2,
        "Distance": 0
    },
    {
        "name": "S2",
        "Biogas": 10,
        "Weight": 50,
        "Fat": 0.08,
        "Cost": 2,
        "Distance": 0
    }
]


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>smartCH4 Biogas Waste Optimization API</title>
        </head>
        <body>
            <h1>smartCH4 Biogas Waste Optimization API</h1>
            <p>Optimize the cost of waste for biogas production using linear programming</p>
            <p>Go to <a href="docs">/docs</a> to see the API documentation.</p>
        </body>
    </html>
    """

@app.post("/solve")
def solve(data: Annotated[
    List[Substrate],
    Body(examples=[EXAMPLES])
], target: Annotated[int, Body(examples=[1000])],
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