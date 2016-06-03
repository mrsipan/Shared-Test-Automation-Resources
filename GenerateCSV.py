from csv import DictWriter
import string
import random
import argparse
from faker import Faker

CENSUS_GENERATION_CONSTANTS = {
    'leters' : 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 
    'field_names' : [
	    'SSN',
	    'First Name',
        'Middle Name',
        'Last Name',
        'Gender',
        'Birth Date',
        'Address 1',
        'Address 2',
        'City',
        'State',
        'ZIP',
        'Mobile Phone',
        'Email',
        'Hire Date',
        'Termination Date',
        'Hours Per Week',
        'Employee Class',
        'Salary',
        'Employee ID',
        'Salary Mode',
        'Country'
	        ],
    'genders' : ['Male', 'Female']
	}


def generate_census_file(path, number_of_records):
    fake = Faker("en_US")
    with open(path, 'wb') as new_census_file:
        writer = DictWriter(new_census_file, CENSUS_GENERATION_CONSTANTS["field_names"])
        created_ssns = set([])
        emp_IDs = set([])
        #faker generated SSNs can be seen as invalid (no idea why).   
        writer.writeheader()
        for index in range(number_of_records):
            census_record = {}
            ssn = '1' + ''.join(str(random.randint(1,9)) for _ in range(8))
            while (ssn in created_ssns):
                ssn = '1' + ''.join(str(random.randint(1,9)) for _ in range(8))
            created_ssns.add(ssn)
            census_record["SSN"] = ssn
            census_record["First Name"] = fake.first_name() + "PerfTest"
            census_record["Last Name"] = fake.last_name()
            census_record["Gender"] = random.choice(CENSUS_GENERATION_CONSTANTS["genders"])
            #Fun fact, this function will call down to the underlying c mktime function. On Unix, there's no problem with providing one before the start of the Unix epoch in 1970.
            #But, on Windows (really?) this will result in a datetime overflow if your start date is before 1970-01-01.
            census_record["Birth Date"] = fake.date_time_between(start_date="-44y", end_date="-26yrs").strftime("%m/%d/%Y")
            census_record["Address 1"] = fake.street_address()
            census_record["Address 2"] = ''
            census_record["City"] = fake.city()
            census_record["State"] = 'IL'
            census_record["ZIP"] = fake.postcode()
            census_record["Mobile Phone"] ='555' + str(random.randint(1000000, 9999999))
            census_record["Email"] = 'PerfTest+' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)) + '@example.com'
            census_record["Hire Date"] = fake.date_time_between(start_date="-180d", end_date="now").strftime("%m/%d/%Y")
            census_record["Termination Date"] = ''
            census_record["Employee Class"] = 'Class 1'
            census_record["Salary"] = fake.random_int(min=40000, max=75000)
            census_record["Hours Per Week"] = 40
            census_record["Salary Mode"] = 'BiWeekly'
            new_emp_id = str(random.randint(1000000, 9999999))
            while new_emp_id in emp_IDs:
                new_emp_id = str(random.randint(1000000, 9999999)) #this is to get unique employee Id
            census_record["Employee ID"] = new_emp_id
            census_record["Country"] = 'USA'
            writer.writerow(census_record)
   
def parse_commandline_arguments():
    parser = argparse.ArgumentParser(description='Take values for running automation')
    parser.add_argument('-n', '--NUM', nargs='?', type=int, help='Number of records to generate [Default: 50]', default=50, metavar='')
    parser.add_argument('-f', '--FILE', nargs='?', type=str, help='Name of the file [Default: GenPerfTest_TC2.csv]', default='GenPerfTest_Users.csv', metavar='')

    return parser.parse_args()
    
def main():
    arguments = parse_commandline_arguments()
    print("Generating Census File {0} with {1} records".format(arguments.FILE, arguments.NUM))
    generate_census_file(arguments.FILE, arguments.NUM)

if __name__ == '__main__':

    main()
