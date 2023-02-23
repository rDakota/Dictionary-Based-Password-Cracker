from os import system
from os import listdir
import sys
from sys import exit

# List of executable files
programs = ['shadow_no_mangle',
            'shadow_case',
            'shadow_number',
            #'shadow_leet',
            'shadow_case_number'
            #'shadow_case_leet',
            #'shadow_number_leet',
            #'shadow_number_leet_case'
           ]

# Lists of tests in the tests/ directory associated with each program
tests = {'shadow_no_mangle':['shadow_no_mangle'],
         'shadow_case':['shadow_case'],
         'shadow_number':['shadow_number'],
#         'shadow_leet':['shadow_leet'],
         'shadow_case_number':['shadow_case_number'],
#         'shadow_case_leet':['shadow_case_leet'],
#         'shadow_number_leet':['shadow_number_leet'],
#         'shadow_number_leet_case':['shadow_number_leet_case']
}

	  
flags = {'shadow_no_mangle':'',
         'shadow_case':'-c',
         'shadow_number':'-n',
         #'shadow_leet':'-l',
         'shadow_case_number':'-c -n',
         #'shadow_case_leet':'-c -l',
         #'shadow_number_leet':'-n -l',
         #'shadow_number_leet_case':'-n -l -c'
}

test_file_list = listdir('./tests')

num_passed = 0
final_return_code = 0

# Remove existing executables
print('\n#####  Removing any existing executables with make clean #####')
system('make clean')

# Build the project
print('\n#####  Building with make  #####')
rc = system('make')
if rc != 0:
	print('Build failed. Exiting.')
	exit(1)
	
# A working build is one of the tests
print('\nBuild passed.'),
num_passed += 1 

for program in programs:
	
	print('\n\n#####  Testing program %s  #####' % program)

	for test in tests[program]:
		
		options = flags[program]
		
		print('\n###  Test %s  ###' % test)
		out_file = test + '.out'
		in_file = test + '.in'
		cmp_file = './tests/' + test + '_truth'
		
		if in_file in test_file_list:
			run_command = './%s < ./tests/%s > %s' % (program, in_file, out_file)
		else:
			run_command = './crack -i ./tests/%s -o %s -d words %s' % (test, out_file, options)
			
		print(run_command)
			
		# diff compares two files and reports if they are different
		# -Z ignores trailing whitespace
		# -q gives same/different reporting
		diff_cmd = 'diff -Z -q %s %s' % (out_file, cmp_file)
		
		system(run_command)
		rc = system(diff_cmd)

		if rc == 0:
			print('Passed.')
			num_passed += 1
		else:
			final_return_code = 1  # Return 1 if any tests fail
			
		#print '\nTest input:'
		#system('cat %s' % './tests/' + in_file)	
		print('\nYour program\'s output:')
		system('cat %s' % out_file)
		print('\n\nExpected output:')
		system('cat %s' % cmp_file)

print('\n\n#####  Final Score  #####')
num_tests = sum([len(x) for x in tests.values()]) + 1
print('You passed %d out of %d tests.' % (num_passed,  num_tests))
print('Percentage = %f' % (float(num_passed) / num_tests* 100))

# Clean up
system('rm *.out')

exit(final_return_code)
