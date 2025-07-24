import time

class EquationEvaluator:
    operations = {
        "+": lambda o_l, o_r: o_l + o_r,
        "-": lambda o_l, o_r: o_l - o_r,
        "*": lambda o_l, o_r: o_l * o_r,
        "/": lambda o_l, o_r: o_l / o_r
    }

    def evaluate(self, operand_l: int, operand_r: int, operator:str):
        try:
            return self.operations[operator](operand_l, operand_r)
        except ZeroDivisionError:
            return None

class Number:
    def __init__(self, value: int, operator = None, parent_l = None, parent_r = None):
        self.value = value
        self.parent_l, self.parent_r, self.operator = parent_l, parent_r, operator
    
    def convert_value_to_int(self):
        self.value = int(self.value)

    def _get_path_recursive(self, num):
        if num.parent_l is None:
            return []
        out = []
        out.extend(self._get_path_recursive(num.parent_l))
        out.extend(self._get_path_recursive(num.parent_r))
        out.append((num.parent_l, num.operator, num.parent_r, num.value))
        return out

    def get_path(self):
        return self._get_path_recursive(self)

    def print_path(self):
        path = self.get_path()
        for operation in path:
            print(f"{operation[0]} {operation[1]} {operation[2]} = {operation[3]}")

    def __str__(self):
        return f"{str(self.value)}"
    def __repr__(self):
        return f"{str(self.parent_l)} {self.operator} {str(self.parent_r)} = {str(self.value)}"
    
    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        if isinstance(other,  Number):
            return self.value == other.value
        return False

    def __add__(self, other):
        return Number(self.value + other.value, operator = "+", parent_l = self, parent_r = other)
    def __sub__(self, other):
        return Number(self.value - other.value, operator = "-", parent_l = self, parent_r = other)
    def __mul__(self, other):
        return Number(self.value * other.value, operator = "*", parent_l = self, parent_r = other)
    def __truediv__(self, other):
        return Number(self.value / other.value, operator = "/", parent_l = self, parent_r = other)
    def __mod__(self, num:int):
        return self.value % num
    def __lt__(self, num:int):
        return self.value < num

class CountleSolver:
    def __init__(self):
        self.start()
        self.evaluator = EquationEvaluator()
        self.solutions = []

    def start(self):
        self.target = int(input("Target number? "))
        self.inputs = list(map(lambda inp: Number(int(inp)),input("Inputs (space separated): ").split()))
    
    def _process_operation(self, left_inp, right_inp, operator):
        out = self.evaluator.evaluate(left_inp, right_inp, operator)
        if out is None:
            return None
        if out % 1 != 0:
            return None
        if out < 0:
            return None
        out.convert_value_to_int()
        return out
    
    def _generate_all_possible_pairs_index(self, curr_inputs) -> list[tuple[int, int]]:
        return [(i, j) for i in range(len(curr_inputs)) for j in range(i+1, len(curr_inputs))]

    def _generate_all_possible_operations(self, curr_inputs) -> list[tuple[int, int, str]]:
        arrangements = self._generate_all_possible_pairs_index(curr_inputs)
        return [(i_l, i_r, operator) for i_l, i_r in arrangements for operator in "+-/*"] + [(i_r, i_l, operator) for i_l, i_r in arrangements for operator in "-/"]
    
    def _get_next_array(self, curr_inputs, ind1, ind2, new_val):
        temp_list = curr_inputs[:ind1] + curr_inputs[ind1+1:]
        if ind2 < ind1:
            return temp_list[:ind2] + temp_list[ind2+1:] + [new_val]
        return temp_list[:ind2-1] + temp_list[ind2:] + [new_val]
    
    def _solve_recursive(self, curr_inputs):
        if len(curr_inputs) < 2:
            return
        
        operations = self._generate_all_possible_operations(curr_inputs)
        for operation in operations:
            left_ind, right_ind, operator = operation
            curr_output = self._process_operation(curr_inputs[left_ind], curr_inputs[right_ind], operator)
            if curr_output is None: # If invalid operation, skip this operation
                continue
            if curr_output == self.target:
                self.solutions.append(curr_output)
                continue
            
            left_ind, right_ind, self._get_next_array(curr_inputs, left_ind, right_ind, curr_output)

            self._solve_recursive(self._get_next_array(curr_inputs, left_ind, right_ind, curr_output))

    def solve(self):
        self._solve_recursive(self.inputs)
        return self.solutions


solver = CountleSolver()
start_time = time.time()
solutions = solver.solve()
end_time = time.time()
print(f"{len(solutions)} solutions found in {str(end_time - start_time)}s!")
for solution in solutions:
    solution.print_path()
    print()