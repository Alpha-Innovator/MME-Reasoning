id_answer_pair_prompt = """Please read the following example. Then extract the answer from the model response and type it at the end of the prompt.
Example: 
    Question: Each cycle represents a number. You need to find out what the three numbers are. Give a possible answer in the format 'cycle id:number'
    Model Response: The possible answer is: A:5, B:1, C:2
    Extracted answer (json format):          
        {{
            "A":5,
            "B":1,
            "C":2
        }}
        
Please extract the answer for the following response:
    Question: {question}
    Model Response: {response}
    You should only output the json without any other texts.
"""

id_answer_pair_prompt_reverse = """Please read the following example. Then extract the answer from the model response and type it at the end of the prompt.
Example: 
    Question: Each cycle (id from 1 to 3) represents a letter. You need to find out what the three numbers are. Give a possible answer in the format 'cycle id:letter'
    Model Response: The possible answer is: 1:A, 2:B, 3:C
    Extracted answer (json format):          
        {{
            "1":"A",
            "2":"B",
            "3":"C"
        }}
        
Please extract the answer for the following response:
    Question: {question}
    Model Response: {response}
    You should only output the json without any other texts.
"""

coordinate_answer_prompt = """Please read the following example. Then extract the answer from the model response and type it at the end of the prompt.
Example1: 
    Question: According to the clues, find the corresponding position. Answer in '(row id (A-C), column id (1-3))' format.
    Model Response: The possible answer is: (A, 1)
    Extracted answer (json format):          
        [
            {{
                "row": "A",
                "column": 1
            }}
        ]
Example2:
    Question: According to the clues, find the two corresponding position. Answer in '(row id (A-C), column id (1-3))' format.
    Model Response: The possible answer is: (A, 1), (B, 3)
    Extracted answer (json format):          
        [
            {{
                "row": "A",
                "column": 1
            }},
            {{
                "row": "B",
                "column": 3
            }}
        ]
        
Please extract the answer for the following response:
    Question: {question}
    Model Response: {response}
    You should only output the json without any other texts.
"""

multiple_answer_prompt = """Please read the following example. Then extract the answer from the model response and type it at the end of the prompt.
Example1: 
    Question: There are six balls (A-F), find two balls that have lower weight. Answer in ball id.
    Model Response: The possible answer is: A, C
    Extracted answer (json format):          
        {{
            "id": ["A", "C"]
        }}
Example2:
    Question: There are six balls (A-F), find a ball that have lower weight. Answer in ball id.
    Model Response: The possible answer is: A
    Extracted answer (json format):          
        {{
            "id": ["A"]
        }}
Please extract the answer for the following response:
    Question: {question}
    Model Response: {response}
    You should only output the json without any other texts.
"""

formula_extraction_prompt = """Please extract the mathematical formula from the following model response and type it at the end of the prompt.
Example:
    Question: What is the right equation to solve the problem?
    Model Response: The right equation to solve the problem is: 2 + 3 = 7
    Extracted answer (json format):          
        {{
            "equation": "2 + 3 = 7"
        }}
Please extract the answer for the following response:
    Question: {question}
    Model Response: {response}
    You should only output the json without any other texts.
"""

choice_prompt = """Please read the following example. Then extract the answer from the model response and type it at the end of the prompt.
Example1: 
    Question: Which answer is right?\n A.1\n B.2\n C.3\n D.4\n Please answer the question and provide the correct option letter, e.g., A, B, C, D, at the end.
    Model Response: The possible answer is: A
    Extracted answer: A
Example2:
    Question: Which answer is right?\n A.1\n B.2\n C.3\n D.4\n Please answer the question and provide all correct option letter, e.g., A, B, C, D, at the end. Find all possible answers.
    Model Response: The possible answer is: A, C
    Extracted answer: [A, C]
        
Please extract the answer for the following response:
    Question: {question}
    Model Response: {response}
    Extracted answer:
    You should only output the answer without any other texts.
"""

open_question_prompt = """Please read the following example. Then extract the answer from the model response and type it at the end of the prompt.
Example1: 
    Question: What value should be? Please answer the question and provide the final value, e.g., 2, 2.10, -3, at the end.
    Model Response: The possible value is -4
    Extracted answer: -4
Example2:
    Question: What value should be? Please answer the question and provide the final value, e.g., 2, 2.10, -3, at the end.
    Model Response: The possible value is $2\sqrt{{3}}$
    Extracted answer: 2\sqrt{{3}}
Example3:
    Question: What value should be? Please answer the question and provide the final value, e.g., 2, 2.10, -3, at the end.
    Model Response: The possible value is 3.28
    Extracted answer: 3.28
        
Please extract the answer for the following response:
    Question: {question}
    Model Response: {response}
    Extracted answer:
    You should only output the answer without any other texts.
"""

hashi_extraction_prompt = """Extract all bridge connections from the Hashi puzzle solution text and format them as a structured JSON list. Follow these rules:

1. **Input**:
   - `solution`: Text describing bridges between islands using various formats (e.g., "c1 - c3", "a1到g1", "between b2 and b4").

2. **Output Requirements**:
   - Return a JSON list of dictionaries in this format:
     ```JSON
     [{{"start": "a1", "end": "b1", "number": 2}}, ...]
     ```
   - Include ALL bridges explicitly described in `solution`.
   - Use 1-based row numbers and letter-based columns (e.g., "c3" not "3c").
   - Normalize coordinate formats (e.g., "(1,c)" → "c1", "d,4" → "d4").

3. **Parsing Rules**:
   - Capture bridge counts (1 or 2) from phrases like:
     - "two bridges"
     - "1 bridge"
     - "double bridge"
   - Handle directional phrases:
     - "from X to Y"
     - "X connects to Y"
     - "X-Y bridge"

4. **Edge Cases**:
   - The bridge corresponding to the following plot will be skipped directly:
     - No bridges can be parsed
     - Ambiguous connections (unclear start/end)
     - Invalid coordinate formats

**Response Format**:
1. Return ONLY the JSON list.
2. Do not include any additional text, explanations, or formatting beyond the JSON list.

**Examples**:
Solution:
"Draw two bridges from a1 to b1, and one bridge between f6-f8"
Output:
[{{"start": "a1", "end": "b1", "number": 2}}, {{"start": "f6", "end": "f8", "number": 1}}]

Solution:
"Connect c3 with d3 using a double bridge"
Output:
[{{"start": "c3", "end": "d3", "number": 2}}]

Now, extract the answer of the following response:
Solution:
{response}
Output:
"""

skyscraper_extraction_prompt = """Extract the final answer from the given solution. The solution will contain a detailed solution to a Sudoku-like puzzle, including step-by-step explanations and a final filled grid representation. Your task is to identify and extract only the final answer, which is presented as a matrix (list of lists or equivalent) at the end of the solution. 

### Requirements:
1. Only return the final filled matrix, formatted as a JSON list of lists.
2. Do not include any additional text, explanations, or formatting beyond the matrix itself.
3. The final answer usually follows phrases such as 'Final Filled Grid' or 'Summary as a Single Filled Matrix'.

### Example 1:
Solution:
To solve the 3x3 Skyscrapers puzzle, we need to place the numbers 1, 2, and 3 in each row and column while adhering to the given clues. Let's break down the solution step by step.\n\n### Step-by-Step Solution:\n\n1. **Analyze the clues:**\n   - Top row: 3, 1, 2\n   - Left column: 2, 2, 1\n   - Right column: 2, 1, 3\n   - Bottom row: 1, 2, 2\n\n2. **Start with the top row:**\n   - The top row has a clue of 3 on the left, meaning all three skyscrapers are visible. This implies the order must be 1, 2, 3 from left to right.\n   - The top row is: [1, 2, 3]\n\n3. **Analyze the left column:**\n   - The left column has a clue of 2 at the top, meaning two skyscrapers are visible. Given the top row is [1, 2, 3], the second row must start with a 3 to block the view of the third row.\n   - The left column is: [1, 3, 2]\n\n4. **Analyze the right column:**\n   - The right column has a clue of 3 at the bottom, meaning all three skyscrapers are visible. This implies the order must be 1, 2, 3 from top to bottom.\n   - The right column is: [3, 2, 1]\n\n5. **Fill in the remaining cells:**\n   - The second row has a clue of 2 on the left, and we already have a 3 in the first column. The remaining cells must be 1 and 2 in some order. Given the right column clue of 2, the second row must be [3, 1, 2].\n   - The third row has a clue of 1 on the left, meaning the first cell must be 2 to block the view of the other cells. The remaining cells must be 3 and 1 in some order. Given the right column clue of 3, the third row must be [2, 3, 1].\n\n### Final Solution:\n\nThe completed 3x3 Skyscrapers puzzle is:\n\n```\n1 2 3\n3 1 2\n2 3 1\n```\n\n### Summary as a single filled matrix:\n\n```python\n[[1, 2, 3], [3, 1, 2], [2, 3, 1]]\n```

Output:
[[1, 2, 3], [3, 1, 2], [2, 3, 1]]

### Example 2:
Solution:
To solve the 4x4 Skyscrapers puzzle, we need to place the numbers 1, 2, 3, and 4 in each row and column while adhering to the given clues. Let's break down the solution step by step.\n\n### Step-by-Step Solution:\n\n1. **Analyze the clues:**\n   - Top row: Clue '2' on the left means we can see 2 skyscrapers from the left.\n   - Bottom row: Clue '4' on the right means we can see 4 skyscrapers from the right.\n   - Left column: Clue '2' on the top means we can see 2 skyscrapers from the top.\n   - Right column: Clue '2' on the bottom means we can see 2 skyscrapers from the bottom.\n\n2. **Start with the bottom row:**\n   - Since we can see 4 skyscrapers from the right, the bottom row must be in ascending order from left to right: [1, 2, 3, 4].\n\n3. **Fill the bottom row:**\n   - Row 4: [1, 2, 3, 4]\n\n4. **Analyze the top row:**\n   - We can see 2 skyscrapers from the left, so the tallest skyscraper (4) must be in the second position from the left to block the view of the third and fourth skyscrapers.\n   - Possible configurations: [3, 4, 1, 2] or [2, 4, 1, 3]\n\n5. **Analyze the left column:**\n   - We can see 2 skyscrapers from the top, so the tallest skyscraper (4) must be in the second position from the top to block the view of the third and fourth skyscrapers.\n   - Possible configurations: [3, 4, 1, 2] or [2, 4, 1, 3]\n\n6. **Combine the clues:**\n   - Top row: [3, 4, 1, 2]\n   - Left column: [3, 4, 1, 2]\n\n7. **Fill the remaining cells:**\n   - Row 1: [3, 4, 1, 2]\n   - Row 2: [4, 1, 2, 3]\n   - Row 3: [2, 3, 4, 1]\n   - Row 4: [1, 2, 3, 4]\n\n### Final Solution:\n\n```\n[[3, 4, 1, 2],\n [4, 1, 2, 3],\n [2, 3, 4, 1],\n [1, 2, 3, 4]]\n```\n\nThis matrix satisfies all the given clues and constraints of the Skyscrapers puzzle.

Output:
[[3, 4, 1, 2], [4, 1, 2, 3], [2, 3, 4, 1], [1, 2, 3, 4]]

Now, please extract the answer for the following solution:
Solution:
{response}

Output:
"""

sudoku_4_extraction_prompt = """Extract the final answer from the given solution. The solution will contain a detailed solution to a Sudoku-like puzzle, including step-by-step explanations and a final filled grid representation. Your task is to identify and extract only the final answer, which is presented as a matrix (list of lists or equivalent) at the end of the solution. 

### Requirements:
1. Only return the final filled matrix, formatted as a JSON list of lists.
2. Do not include any additional text, explanations, or formatting beyond the matrix itself.
3. The final answer usually follows phrases such as 'Final Filled Grid' or 'Summary as a Single Filled Matrix'.

### Example 1:
Solution:
To solve the given Jigsaw Sudoku puzzle, we need to ensure that each row, each column, and each 2x2 sub-grid contains the digits 1 through 4 exactly once. Let's fill in the grid step by step.\n\nStep-by-Step Solution:\n1. **Identify the given numbers and their positions:**\n   - Top row: 1, 3\n   - Second row: 3\n   - Third row: (empty)\n   - Fourth row: 2, 3, 1\n\n2. **Fill in the top row:**\n   - The top row already has 1 and 3. The remaining digits are 2 and 4.\n   - The first column already has a 3, so the first cell in the top row cannot be 3. Therefore, it must be 2.\n   - The fourth column already has a 3, so the fourth cell in the top row cannot be 3. Therefore, it must be 4.\n   - Top row: [2, 1, 4, 3]\n\n### Final Filled Matrix:\n[[2, 1, 4, 3], [1, 4, 2, 3], [4, 2, 1, 3], [2, 3, 4, 1]]

Output:
[[2, 1, 4, 3], [1, 4, 2, 3], [4, 2, 1, 3], [2, 3, 4, 1]]

### Example 2:
Solution:
1. **Identify the given numbers and their positions:**\n   - Top row: 1, 3\n   - Second row: 3\n   - Third row: (empty)\n   - Fourth row: 2, 3, 1\n\n2. **Fill in the top row:**\n   - The top row already has 1 and 3. The remaining digits are 2 and 4.\n   - The first column already has a 3, so the first cell in the top row cannot be 3. Therefore, it must be 2.\n   - The fourth column already has a 3, so the fourth cell in the top row cannot be 3. Therefore, it must be 4.\n   - Top row: 2, 1, 4, 3\n\n3. **Fill in the second row:**\n   - The second row already has a 3. The remaining digits are 1, 2, and 4.\n   - The first column already has a 2 and a 3, so the first cell in the second row cannot be 2 or 3. Therefore, it must be 1.\n   - The second column already has a 1, so the second cell in the second row cannot be 1. Therefore, it must be 4.\n   - The fourth column already has a 3 and a 4, so the fourth cell in the second row cannot be 3 or 4. Therefore, it must be 2.\n   - Second row: 1, 4, 2, 3\n\n4. **Fill in the third row:**\n   - The third row is empty. The remaining digits are 1, 2, 3, and 4.\n   - The first column already has a 2 and a 1, so the first cell in the third row cannot be 2 or 1. Therefore, it must be 4.\n   - The second column already has a 1 and a 4, so the second cell in the third row cannot be 1 or 4. Therefore, it must be 2.\n   - The third column already has a 4 and a 2, so the third cell in the third row cannot be 4 or 2. Therefore, it must be 1.\n   - The fourth column already has a 3 and a 2, so the fourth cell in the third row cannot be 3 or 2. Therefore, it must be 3.\n   - Third row: 4, 2, 1, 3\n\n5. **Fill in the fourth row:**\n   - The fourth row already has 2, 3, and 1. The remaining digit is 4.\n   - Fourth row: 2, 3, 4, 1\n\n### Final Filled Matrix:\n```python\n[\n    [2, 1, 4, 3],\n    [1, 4, 2, 3],\n    [4, 2, 1, 3],\n    [2, 3, 4, 1]\n]\n```\n\n### Summary:\nThe completed Jigsaw Sudoku puzzle is:\n```python\n[\n    [2, 1, 4, 3],\n    [1, 4, 2, 3],\n    [4, 2, 1, 3],\n    [2, 3, 4, 1]\n]\n```

Output:
[[2, 1, 4, 3],[1, 4, 2, 3],[4, 2, 1, 3],[2, 3, 4, 1]]

Now, extract the answer of the following response:

Solution:
{response}

Output:
"""

sudoku_6_extraction_prompt = """Extract the final answer from the given solution. The solution will contain a detailed solution to a Sudoku-like puzzle, including step-by-step explanations and a final filled grid representation. Your task is to identify and extract only the final answer, which is presented as a matrix (list of lists or equivalent) at the end of the solution. 

### Requirements:
1. Only return the final filled matrix, formatted as a JSON list of lists.
2. Do not include any additional text, explanations, or formatting beyond the matrix itself.
3. The final answer usually follows phrases such as 'Final Filled Grid' or 'Summary as a Single Filled Matrix'.

### Example 1:
Solution:
To solve the given Jigsaw Sudoku puzzle, we need to ensure that each row, each column, and each 2x3 sub-grid contains the digits 1 through 6 exactly once. Let's solve it step by step.\n\n### Step-by-Step Solution:\n\n1. **Identify the sub-grids and initial constraints:**\n   - The grid is divided into 2x3 sub-grids.\n   - We need to fill in the empty cells while satisfying the Sudoku rules.\n\n2. **Fill in the first row:**\n   - The first row has the digits 2 and 4 already placed.\n   - The remaining digits are 1, 3, 5, and 6.\n   - Considering the constraints of the sub-grids and columns, we can place the digits as follows:\n     - First row: [5, 3, 2, 1, 6, 4]\n\n3. **Fill in the second row:**\n   - The second row has the digits 6 and 1 already placed.\n   - The remaining digits are 2, 3, 4, and 5.\n   - Considering the constraints, we can place the digits as follows:\n     - Second row: [4, 6, 1, 5, 3, 2]\n\n4. **Fill in the third row:**\n   - The third row has the digits 1, 3, and 6 already placed.\n   - The remaining digits are 2, 4, and 5.\n   - Considering the constraints, we can place the digits as follows:\n     - Third row: [1, 3, 5, 6, 2, 4]\n\n5. **Fill in the fourth row:**\n   - The fourth row has the digits 6, 3, and 1 already placed.\n   - The remaining digits are 2, 4, and 5.\n   - Considering the constraints, we can place the digits as follows:\n     - Fourth row: [2, 5, 6, 4, 3, 1]\n\n6. **Fill in the fifth row:**\n   - The fifth row has the digits 4 and 2 already placed.\n   - The remaining digits are 1, 3, 5, and 6.\n   - Considering the constraints, we can place the digits as follows:\n     - Fifth row: [3, 1, 4, 2, 5, 6]\n\n7. **Fill in the sixth row:**\n   - The sixth row has the digits 6 and 3 already placed.\n   - The remaining digits are 1, 2, 4, and 5.\n   - Considering the constraints, we can place the digits as follows:\n     - Sixth row: [6, 2, 1, 3, 4, 5]\n\n### Final Filled Matrix:\n\n```python\n[\n    [5, 3, 2, 1, 6, 4],\n    [4, 6, 1, 5, 3, 2],\n    [1, 3, 5, 6, 2, 4],\n    [2, 5, 6, 4, 3, 1],\n    [3, 1, 4, 2, 5, 6],\n    [6, 2, 1, 3, 4, 5]\n]\n```

Output:
[[5, 3, 2, 1, 6, 4],[4, 6, 1, 5, 3, 2],[1, 3, 5, 6, 2, 4],[2, 5, 6, 4, 3, 1],[3, 1, 4, 2, 5, 6],[6, 2, 1, 3, 4, 5]]

### Example 2:
Solution:
To solve this 6×6 Jigsaw Sudoku puzzle, we need to ensure that:\n\n1. Each row contains the digits 1–6 exactly once.\n2. Each column contains the digits 1–6 exactly once.\n3. Each 2×3 sub-grid contains the digits 1–6 exactly once.\n\nHere is the completed solution:\n\n### Completed Sudoku Grid:\n```\n1 3 4 2 5 6\n6 2 5 1 3 4\n5 6 2 3 4 1\n3 4 6 5 1 2\n4 5 1 6 2 3\n2 1 3 4 6 5\n```\n\n### Summary as a Matrix:\n```python\n[\n    [1, 3, 4, 2, 5, 6],\n    [6, 2, 5, 1, 3, 4],\n    [5, 6, 2, 3, 4, 1],\n    [3, 4, 6, 5, 1, 2],\n    [4, 5, 1, 6, 2, 3],\n    [2, 1, 3, 4, 6, 5]\n]\n```

Output:
[[1, 3, 4, 2, 5, 6],[6, 2, 5, 1, 3, 4],[5, 6, 2, 3, 4, 1],[3, 4, 6, 5, 1, 2],[4, 5, 1, 6, 2, 3],[2, 1, 3, 4, 6, 5]]

Now, extract the answer of the following response:

Solution:
{response}

Output:
"""

yinyang_extraction_prompt = """Extract the final answer from the given solution. The solution will contain a detailed solution to a Sudoku-like puzzle, including step-by-step explanations and a final filled grid representation. Your task is to identify and extract only the final answer, which is presented as a matrix (list of lists or equivalent) at the end of the solution. 

### Requirements:
1. Only return the final filled matrix, formatted as a JSON list of lists.
2. Do not include any additional text, explanations, or formatting beyond the matrix itself.
3. The final answer usually follows phrases such as 'Final Filled Grid' or 'Summary as a Single Filled Matrix'.

### Example 1:
Solution:
To solve the Yin-Yang puzzle, we need to place black and white stones at the intersections of the grid lines while adhering to the given rules. Let's analyze the current state of the grid and determine the placement of the remaining stones.\n\n### Step-by-Step Solution:\n\n1. **Initial Setup:**\n   - The grid is a 6x6 matrix.\n   - Some cells already have black (1) and white (0) stones.\n\n2. **Rule Analysis:**\n   - All black stones must be orthogonally connected.\n   - All white stones must be orthogonally connected.\n   - No 2x2 region can be monochromatic.\n   - Existing stones cannot be moved.\n\n3. **Placement Strategy:**\n   - Start by ensuring the connectivity of black and white stones.\n   - Avoid creating monochromatic 2x2 regions.\n\n### Detailed Placement:\n\n- **Top-left corner (a1):**\n  - Place a white stone to avoid a monochromatic 2x2 region with the black stone at (b1).\n\n- **Top-right corner (f1):**\n  - Place a white stone to avoid a monochromatic 2x2 region with the black stone at (e1).\n\n- **Middle section:**\n  - Ensure connectivity of black and white stones while avoiding monochromatic 2x2 regions.\n\n### Final Matrix:\n\nAfter placing the stones according to the rules, the final matrix is:\n\n```\n[\n  [0, 1, 0, 1, 0, 0],\n  [0, 0, 1, 1, 0, 0],\n  [1, 0, 1, 0, 1, 0],\n  [0, 1, 0, 1, 0, 1],\n  [0, 0, 1, 0, 1, 0],\n  [1, 0, 0, 1, 0, 0]\n]\n```\n\n### Summary:\n\nThe completed solution for the Yin-Yang puzzle is represented as a single filled matrix:\n\n```python\n[\n  [0, 1, 0, 1, 0, 0],\n  [0, 0, 1, 1, 0, 0],\n  [1, 0, 1, 0, 1, 0],\n  [0, 1, 0, 1, 0, 1],\n  [0, 0, 1, 0, 1, 0],\n  [1, 0, 0, 1, 0, 0]\n]\n```

Output:
[[0, 1, 0, 1, 0, 0],[0, 0, 1, 1, 0, 0],[1, 0, 1, 0, 1, 0],[0, 1, 0, 1, 0, 1],[0, 0, 1, 0, 1, 0],[1, 0, 0, 1, 0, 0]]

### Example 2:
Solution:
To solve the Yin-Yang puzzle, we need to ensure that the rules are followed:\n\n1. All black stones form a single orthogonally connected group.\n2. All white stones form a single orthogonally connected group.\n3. No 2x2 region is monochromatic.\n4. The positions of the pre-placed stones cannot be changed.\n\n### Step-by-Step Solution:\n\n#### Initial Setup:\nThe given grid is a 6x6 grid with some pre-placed black and white stones. We\'ll represent the grid as follows:\n- "1" for black stones.\n- "0" for white stones.\n- Empty cells will be filled as we solve the puzzle.\n\n#### Pre-placed Stones:\nFrom the diagram:\n- Black stones ("1") are at: (a1, b1, c1, c2, d2, d3, e3).\n- White stones ("0") are at: (a3, a4, a5, b4, b5, c4, d4, e4).\n\n#### Solving the Puzzle:\nWe will fill the remaining cells while ensuring the rules are satisfied.\n\n---\n\n### Final Solution:\nAfter solving, the completed grid is as follows:\n\n```\n1 1 1 0 0 0\n0 1 0 1 0 0\n0 1 0 1 1 0\n0 0 0 1 0 1\n0 0 0 0 0 1\n1 0 0 0 1 1\n```\n\n### Summary:\nThe solution as a 6x6 matrix is:\n\n```python\n[\n    [1, 1, 1, 0, 0, 0],\n    [0, 1, 0, 1, 0, 0],\n    [0, 1, 0, 1, 1, 0],\n    [0, 0, 0, 1, 0, 1],\n    [0, 0, 0, 0, 0, 1],\n    [1, 0, 0, 0, 1, 1]\n]\n```

Output:
[[1, 1, 1, 0, 0, 0],[0, 1, 0, 1, 0, 0],[0, 1, 0, 1, 1, 0],[0, 0, 0, 1, 0, 1],[0, 0, 0, 0, 0, 1],[1, 0, 0, 0, 1, 1]]

Now, extract the answer of the following response:
Solution:
{response}

Output:
"""

points24_prompt = """
Please read the following examples. Then extract the final formula from the answer to the 24-point game, and type it at the end of the prompt. In the cards, K stands for 13, Q stands for 12, J stands for 11, and A stands for 1. Note you need to use * to represent multiplication sign, / to represent division sign.
Example1:
    Question: Given four playing cards (A, 8, 9, K), each with a value, use any combination of addition, subtraction, multiplication, and division to make the number 24. You must use each card exactly once. Give the final answer as a formula.
    Model Response: The possible answer is (K - 9 - A) × 8 = 24
    Extracted answer: (13-9-1)*8=24
Example2:
    Question: Given four playing cards (3, 8, 9, A), each with a value, use any combination of addition, subtraction, multiplication, and division to make the number 24. You must use each card exactly once. Give the final answer as a formula.
    Model Response: The possible answer is 9 \\div 3 \\times A \\times 8 = 24
    Extracted answer: 9/3*1*8=24

Please extract the final formula from for the following response:
    Question: {question}
    Model Response: {response}
    Extracted answer:
    You should only output the final formula from without any other texts.
"""

prompts = {
    "id_answer_pair_prompt": id_answer_pair_prompt,
    "id_answer_pair_prompt_reverse": id_answer_pair_prompt_reverse,
    "coordinate_answer_prompt": coordinate_answer_prompt,
    "multiple_answer_prompt": multiple_answer_prompt,
    "formula_extraction_prompt": formula_extraction_prompt,
    "choice_prompt": choice_prompt,
    "open_question_prompt": open_question_prompt,
    "hashi_extraction_prompt": hashi_extraction_prompt,
    "skyscraper_extraction_prompt": skyscraper_extraction_prompt,
    "sudoku_4_extraction_prompt": sudoku_4_extraction_prompt,
    "sudoku_6_extraction_prompt": sudoku_6_extraction_prompt,
    "yinyang_extraction_prompt": yinyang_extraction_prompt,
    "points24_prompt": points24_prompt
}