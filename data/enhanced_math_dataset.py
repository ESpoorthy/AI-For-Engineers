"""
Enhanced Mathematical Dataset Generator
Creates comprehensive training data for step-by-step mathematical reasoning
"""

import json
import random
import numpy as np
from typing import List, Dict


class MathDatasetGenerator:
    """Generate comprehensive mathematical training data"""
    
    def __init__(self):
        self.problem_types = [
            'calculus', 'algebra', 'geometry', 'statistics', 
            'linear_algebra', 'differential_equations', 'discrete_math'
        ]
    
    def generate_calculus_problems(self) -> List[Dict]:
        """Generate calculus problems with step-by-step solutions"""
        problems = []
        
        # Integration problems
        integration_problems = [
            {
                "question": "Find the integral of 3x² + 2x - 5 dx",
                "answer": "Step 1: Identify this as a polynomial integration problem. Step 2: Apply the power rule: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C. Step 3: Integrate each term separately: ∫3x² dx = 3∫x² dx = 3(x³/3) = x³. Step 4: ∫2x dx = 2∫x dx = 2(x²/2) = x². Step 5: ∫(-5) dx = -5x. Step 6: Combine all terms: x³ + x² - 5x + C, where C is the constant of integration. Step 7: Verification: d/dx(x³ + x² - 5x + C) = 3x² + 2x - 5 ✓"
            },
            {
                "question": "Evaluate ∫(2x + 1)³ dx using substitution",
                "answer": "Step 1: Identify this as a composite function suitable for u-substitution. Step 2: Let u = 2x + 1, then du = 2 dx, so dx = du/2. Step 3: Substitute into the integral: ∫u³ · (du/2) = (1/2)∫u³ du. Step 4: Apply the power rule: (1/2) · (u⁴/4) = u⁴/8. Step 5: Substitute back: (2x + 1)⁴/8 + C. Step 6: Verification: d/dx[(2x + 1)⁴/8] = (1/8) · 4(2x + 1)³ · 2 = (2x + 1)³ ✓"
            },
            {
                "question": "Find ∫x·ln(x) dx using integration by parts",
                "answer": "Step 1: Recognize this requires integration by parts: ∫u dv = uv - ∫v du. Step 2: Choose u = ln(x) and dv = x dx (choose u as the function that simplifies when differentiated). Step 3: Find du = (1/x) dx and v = x²/2. Step 4: Apply the formula: ∫x·ln(x) dx = ln(x)·(x²/2) - ∫(x²/2)·(1/x) dx. Step 5: Simplify the remaining integral: ∫(x²/2)·(1/x) dx = ∫(x/2) dx = x²/4. Step 6: Complete the solution: (x²/2)ln(x) - x²/4 + C. Step 7: Factor out x²/4: (x²/4)[2ln(x) - 1] + C"
            }
        ]
        
        # Differentiation problems
        differentiation_problems = [
            {
                "question": "Find the derivative of f(x) = (3x² + 1)⁵ using the chain rule",
                "answer": "Step 1: Identify this as a composite function f(g(x)) where f(u) = u⁵ and g(x) = 3x² + 1. Step 2: Apply the chain rule: d/dx[f(g(x))] = f'(g(x)) · g'(x). Step 3: Find the outer derivative: f'(u) = 5u⁴, so f'(g(x)) = 5(3x² + 1)⁴. Step 4: Find the inner derivative: g'(x) = d/dx(3x² + 1) = 6x. Step 5: Multiply the results: f'(x) = 5(3x² + 1)⁴ · 6x = 30x(3x² + 1)⁴. Step 6: Verification: This can be checked by expanding (3x² + 1)⁵ and differentiating term by term."
            },
            {
                "question": "Find dy/dx if y = x³sin(x) using the product rule",
                "answer": "Step 1: Identify this as a product of two functions: u = x³ and v = sin(x). Step 2: Apply the product rule: d/dx[uv] = u'v + uv'. Step 3: Find u' = d/dx(x³) = 3x². Step 4: Find v' = d/dx(sin(x)) = cos(x). Step 5: Apply the formula: dy/dx = (3x²)(sin(x)) + (x³)(cos(x)). Step 6: Simplify: dy/dx = 3x²sin(x) + x³cos(x). Step 7: Factor out x²: dy/dx = x²(3sin(x) + x·cos(x))"
            }
        ]
        
        problems.extend(integration_problems)
        problems.extend(differentiation_problems)
        return problems
    
    def generate_algebra_problems(self) -> List[Dict]:
        """Generate algebra problems with detailed solutions"""
        problems = [
            {
                "question": "Solve the quadratic equation 2x² - 7x + 3 = 0",
                "answer": "Step 1: Identify this as a quadratic equation in standard form ax² + bx + c = 0 where a=2, b=-7, c=3. Step 2: Apply the quadratic formula: x = [-b ± √(b² - 4ac)] / (2a). Step 3: Calculate the discriminant: b² - 4ac = (-7)² - 4(2)(3) = 49 - 24 = 25. Step 4: Since the discriminant is positive, we have two real solutions. Step 5: Substitute values: x = [7 ± √25] / (2·2) = [7 ± 5] / 4. Step 6: Find both solutions: x₁ = (7 + 5)/4 = 12/4 = 3, x₂ = (7 - 5)/4 = 2/4 = 1/2. Step 7: Verification: 2(3)² - 7(3) + 3 = 18 - 21 + 3 = 0 ✓, 2(1/2)² - 7(1/2) + 3 = 1/2 - 7/2 + 3 = 0 ✓"
            },
            {
                "question": "Factor the expression x³ - 8x² + 15x completely",
                "answer": "Step 1: Look for common factors first. All terms contain x, so factor out x: x(x² - 8x + 15). Step 2: Now factor the quadratic x² - 8x + 15. Step 3: Find two numbers that multiply to 15 and add to -8: -3 and -5 work because (-3)(-5) = 15 and (-3) + (-5) = -8. Step 4: Factor the quadratic: x² - 8x + 15 = (x - 3)(x - 5). Step 5: Complete factorization: x³ - 8x² + 15x = x(x - 3)(x - 5). Step 6: Verification: Expand x(x - 3)(x - 5) = x[(x - 3)(x - 5)] = x[x² - 5x - 3x + 15] = x[x² - 8x + 15] = x³ - 8x² + 15x ✓"
            },
            {
                "question": "Solve the system of equations: 2x + 3y = 7 and x - y = 1",
                "answer": "Step 1: Choose the substitution method since the second equation easily solves for x. Step 2: From x - y = 1, solve for x: x = y + 1. Step 3: Substitute x = y + 1 into the first equation: 2(y + 1) + 3y = 7. Step 4: Expand and simplify: 2y + 2 + 3y = 7, which gives 5y + 2 = 7. Step 5: Solve for y: 5y = 5, so y = 1. Step 6: Find x using x = y + 1: x = 1 + 1 = 2. Step 7: Verification: Check both equations: 2(2) + 3(1) = 4 + 3 = 7 ✓, 2 - 1 = 1 ✓"
            }
        ]
        return problems
    
    def generate_geometry_problems(self) -> List[Dict]:
        """Generate geometry problems with step-by-step solutions"""
        problems = [
            {
                "question": "Find the area of a triangle with sides 5, 12, and 13 units",
                "answer": "Step 1: Check if this is a right triangle by testing if it satisfies the Pythagorean theorem: a² + b² = c². Step 2: Test: 5² + 12² = 25 + 144 = 169 = 13². Since this is true, it's a right triangle. Step 3: For a right triangle, Area = (1/2) × base × height, where the two shorter sides are the base and height. Step 4: Area = (1/2) × 5 × 12 = (1/2) × 60 = 30 square units. Step 5: Alternative verification using Heron's formula: s = (5 + 12 + 13)/2 = 15. Step 6: Area = √[s(s-a)(s-b)(s-c)] = √[15(15-5)(15-12)(15-13)] = √[15×10×3×2] = √900 = 30 ✓"
            },
            {
                "question": "Find the volume of a cylinder with radius 4 cm and height 10 cm",
                "answer": "Step 1: Recall the formula for the volume of a cylinder: V = πr²h, where r is radius and h is height. Step 2: Identify the given values: radius r = 4 cm, height h = 10 cm. Step 3: Substitute into the formula: V = π × (4)² × 10. Step 4: Calculate: V = π × 16 × 10 = 160π cubic cm. Step 5: For numerical approximation, use π ≈ 3.14159: V ≈ 160 × 3.14159 ≈ 502.65 cubic cm. Step 6: The exact answer is 160π cm³, approximately 502.65 cm³."
            }
        ]
        return problems
    
    def generate_statistics_problems(self) -> List[Dict]:
        """Generate statistics and probability problems"""
        problems = [
            {
                "question": "Find the mean, median, and mode of the dataset: 2, 4, 4, 6, 8, 8, 8, 10",
                "answer": "Step 1: Arrange the data in ascending order (already done): 2, 4, 4, 6, 8, 8, 8, 10. Step 2: Find the mean by adding all values and dividing by the count: Sum = 2+4+4+6+8+8+8+10 = 50, Count = 8. Step 3: Mean = 50/8 = 6.25. Step 4: Find the median (middle value): With 8 values, median is the average of the 4th and 5th values. Step 5: 4th value = 6, 5th value = 8, so Median = (6+8)/2 = 7. Step 6: Find the mode (most frequent value): 8 appears 3 times, 4 appears 2 times, others appear once. Step 7: Mode = 8. Summary: Mean = 6.25, Median = 7, Mode = 8."
            },
            {
                "question": "A bag contains 3 red balls and 5 blue balls. What's the probability of drawing 2 red balls without replacement?",
                "answer": "Step 1: Identify this as a probability problem without replacement. Total balls = 3 red + 5 blue = 8 balls. Step 2: Find probability of first red ball: P(1st red) = 3/8. Step 3: After drawing one red ball, we have 2 red and 5 blue remaining (7 total). Step 4: Find probability of second red ball given first was red: P(2nd red | 1st red) = 2/7. Step 5: Apply multiplication rule for dependent events: P(2 red) = P(1st red) × P(2nd red | 1st red). Step 6: Calculate: P(2 red) = (3/8) × (2/7) = 6/56 = 3/28. Step 7: Convert to decimal: 3/28 ≈ 0.107 or about 10.7%."
            }
        ]
        return problems
    
    def generate_linear_algebra_problems(self) -> List[Dict]:
        """Generate linear algebra problems"""
        problems = [
            {
                "question": "Find the determinant of the 2×2 matrix [[3, 1], [2, 4]]",
                "answer": "Step 1: Recall the formula for a 2×2 matrix determinant: det([[a,b],[c,d]]) = ad - bc. Step 2: Identify the matrix elements: a = 3, b = 1, c = 2, d = 4. Step 3: Apply the formula: det = (3)(4) - (1)(2) = 12 - 2 = 10. Step 4: Therefore, the determinant is 10. Step 5: Geometric interpretation: The determinant represents the area of the parallelogram formed by the column vectors (3,2) and (1,4)."
            },
            {
                "question": "Find the dot product of vectors u = (2, -1, 3) and v = (1, 4, -2)",
                "answer": "Step 1: Recall the dot product formula: u·v = u₁v₁ + u₂v₂ + u₃v₃. Step 2: Identify vector components: u = (2, -1, 3), v = (1, 4, -2). Step 3: Calculate each term: u₁v₁ = (2)(1) = 2, u₂v₂ = (-1)(4) = -4, u₃v₃ = (3)(-2) = -6. Step 4: Sum the terms: u·v = 2 + (-4) + (-6) = 2 - 4 - 6 = -8. Step 5: The dot product is -8. Step 6: Since the dot product is negative, the angle between the vectors is obtuse (greater than 90°)."
            }
        ]
        return problems
    
    def generate_comprehensive_dataset(self, num_problems_per_type: int = 20) -> List[Dict]:
        """Generate a comprehensive mathematical dataset"""
        all_problems = []
        
        # Generate problems for each type
        generators = [
            self.generate_calculus_problems,
            self.generate_algebra_problems,
            self.generate_geometry_problems,
            self.generate_statistics_problems,
            self.generate_linear_algebra_problems
        ]
        
        for generator in generators:
            problems = generator()
            # Extend with variations if needed
            while len(problems) < num_problems_per_type:
                problems.extend(generator())
            all_problems.extend(problems[:num_problems_per_type])
        
        # Add some advanced problems
        advanced_problems = self.generate_advanced_problems()
        all_problems.extend(advanced_problems)
        
        # Shuffle the dataset
        random.shuffle(all_problems)
        
        return all_problems
    
    def generate_advanced_problems(self) -> List[Dict]:
        """Generate advanced mathematical problems"""
        problems = [
            {
                "question": "Solve the differential equation dy/dx = y/x with initial condition y(1) = 2",
                "answer": "Step 1: Recognize this as a separable differential equation. Step 2: Separate variables: dy/y = dx/x. Step 3: Integrate both sides: ∫(1/y)dy = ∫(1/x)dx. Step 4: Evaluate integrals: ln|y| = ln|x| + C₁. Step 5: Solve for y: |y| = e^(ln|x| + C₁) = e^C₁ · |x|. Step 6: Let C = ±e^C₁, so y = Cx. Step 7: Apply initial condition y(1) = 2: 2 = C(1), so C = 2. Step 8: The particular solution is y = 2x. Step 9: Verification: dy/dx = 2, y/x = 2x/x = 2, so dy/dx = y/x ✓"
            },
            {
                "question": "Find the limit of (sin(x) - x)/x³ as x approaches 0",
                "answer": "Step 1: Direct substitution gives 0/0, an indeterminate form, so we need L'Hôpital's rule or Taylor series. Step 2: Use Taylor series: sin(x) = x - x³/6 + x⁵/120 - ... Step 3: Substitute: sin(x) - x = (x - x³/6 + x⁵/120 - ...) - x = -x³/6 + x⁵/120 - ... Step 4: Form the fraction: (sin(x) - x)/x³ = (-x³/6 + x⁵/120 - ...)/x³. Step 5: Simplify: = -1/6 + x²/120 - ... Step 6: As x → 0, all terms with positive powers of x approach 0. Step 7: Therefore, lim(x→0) (sin(x) - x)/x³ = -1/6."
            }
        ]
        return problems
    
    def save_dataset(self, filename: str = "data/processed/comprehensive_math_dataset.json"):
        """Save the generated dataset to a JSON file"""
        dataset = self.generate_comprehensive_dataset()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        
        print(f"Generated {len(dataset)} mathematical problems and saved to {filename}")
        return dataset


if __name__ == "__main__":
    generator = MathDatasetGenerator()
    dataset = generator.save_dataset()
    
    # Print some statistics
    print(f"\nDataset Statistics:")
    print(f"Total problems: {len(dataset)}")
    
    # Count problem types
    problem_types = {}
    for problem in dataset:
        # Simple heuristic to categorize problems
        question = problem['question'].lower()
        if 'integral' in question or 'integrate' in question:
            problem_types['Integration'] = problem_types.get('Integration', 0) + 1
        elif 'derivative' in question or 'differentiate' in question:
            problem_types['Differentiation'] = problem_types.get('Differentiation', 0) + 1
        elif 'solve' in question and ('equation' in question or '=' in question):
            problem_types['Equations'] = problem_types.get('Equations', 0) + 1
        elif 'matrix' in question or 'determinant' in question or 'vector' in question:
            problem_types['Linear Algebra'] = problem_types.get('Linear Algebra', 0) + 1
        elif 'probability' in question or 'mean' in question or 'median' in question:
            problem_types['Statistics'] = problem_types.get('Statistics', 0) + 1
        elif 'area' in question or 'volume' in question or 'triangle' in question:
            problem_types['Geometry'] = problem_types.get('Geometry', 0) + 1
        else:
            problem_types['Other'] = problem_types.get('Other', 0) + 1
    
    for ptype, count in problem_types.items():
        print(f"{ptype}: {count} problems")