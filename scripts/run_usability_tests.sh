#!/bin/bash

# Initialize counters
success_count=0
failure_count=0

# Function to run a test and update counters
run_test() {
    local test_name=$1
    local command=$2

    echo "Running test: $test_name"
    eval "$command"
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "Test $test_name passed!"
        ((success_count++))
    else
        echo "Test $test_name failed with exit code $exit_code"
        ((failure_count++))
    fi
    echo
}

# Run tests
run_test "git test" "git clone https://github.com/AIDASoft/DD4hep --depth 1"
cat <<EOF > hello.cpp
#include <iostream>
int main() {
    std::cout << "Hello, world!" << std::endl;
    return 0;
}
EOF
run_test "c++ test" "g++ -o hello hello.cpp && ./hello"
cat <<EOF > hello.f
      program hello
      print *, "Hello, world!"
      end program hello
EOF
run_test "fortran test" "gfortran -o hello hello.f && ./hello"
run_test "Python test" "python -c 'print(\"Hello, world!\")'"
run_test "Python3 test" "python3 -c 'print(\"Hello, world!\")'"
run_test "Numpy test" "python -c 'import numpy as np; np.random.seed(0); print(np.random.rand(3, 3))'"
run_test "Matplotlib test" "python -c 'import matplotlib.pyplot as plt; plt.plot([1, 2, 3], [1, 2, 3]); plt.show()'"
run_test "Pandas test" "python -c 'import pandas as pd; print(pd.DataFrame([[1, 2], [3, 4]]))'"

cat > macro.C <<EOF
{
    int a = 10;
    int b = 5;
    int sum = a + b;
    std::cout << "The sum of " << a << " and " << b << " is " << sum << std::endl;
    return 0;
}
EOF
run_test "ROOT test" "root -b -q -l macro.C"
run_test "clang-format test" "echo 'int main() { return 0 ; }' | clang-format | diff - <(echo 'int main() { return 0; }')"

run_test "DD4hep test" "ddsim --compactFile DD4hep/DDDetectors/compact/SiD.xml -G -N 1 --gun.particle=mu- --gun.distribution uniform --gun.energy '1*GeV' -O muons.slcio"
# run_test "podio test" "podio-dump muons.slcio"
# run_test "edm4hep test"
# run_test "k4fwcore test" "k4run -n 10 --input muons.slcio --output output.slcio --processors k4FWCoreTestProcessor"
# run_test "whizard test" "whizard -r 0 -N 10 -f $LCGEO/CLIC/models/CLIC_o3_v14/ee_ZH_Zmumu_Hbb.evt -o test.stdhep"


# Report results
echo "Tests completed:"
echo "Successes: $success_count"
echo "Failures: $failure_count"

# Fail if there were any failures
if [ $failure_count -gt 0 ]; then
    echo "There were test failures!"
    exit 1
else
    echo "All tests passed!"
    exit 0
fi
