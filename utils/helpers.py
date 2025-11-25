# utils/helpers.py
from core.models import Book, User
from persistence.store import DataStore

# Branding
COLLEGE_NAME = "IT College of Engineering, Delhi"
COLLEGE_EMAIL = "library@itcollege.ac.in"

def short_id(s):
    """Display-friendly ID: last 6 digits of numeric ID (string)."""
    s = str(s)
    return s[-6:]

def ensure_sample_data():
    books = DataStore.load_books()
    if books:
        return

    # large sample list (keeps consistent with earlier)
    samples = [
        Book(title="Engineering Mathematics", author="R. K. Jain", publisher="TechPub", year=2019, category="Mathematics", copies=8),
        Book(title="Programming in C", author="Kernighan & Ritchie", publisher="CJ Press", year=2018, category="Computer Science", copies=6),
        Book(title="Data Structures and Algorithms", author="Lipsa", publisher="IndieBooks", year=2020, category="Computer Science", copies=10),
        Book(title="Digital Logic Design", author="M. Morris Mano", publisher="Pearson", year=2017, category="Electronics", copies=5),
        Book(title="Signals and Systems", author="A. V. Oppenheim", publisher="McGraw-Hill", year=2015, category="Electronics", copies=4),
        Book(title="Operating Systems", author="A. Silberschatz", publisher="Wiley", year=2019, category="Computer Science", copies=7),
        Book(title="Database Systems", author="Ramakrishnan", publisher="TMH", year=2021, category="Computer Science", copies=7),
        Book(title="Thermodynamics", author="P. K. Nag", publisher="Hill", year=2016, category="Mechanical", copies=5),
        Book(title="Computer Networks", author="A. S. Tanenbaum", publisher="Pearson", year=2018, category="Computer Science", copies=6),
        Book(title="Design of Machine Elements", author="V. B. Bhandari", publisher="McGraw-Hill", year=2016, category="Mechanical", copies=4),
        Book(title="Compiler Design", author="Aho & Ullman", publisher="Pearson", year=2013, category="Computer Science", copies=3),
        Book(title="Power Systems", author="C. L. Wadhwa", publisher="NewAge", year=2012, category="Electrical", copies=4),
        Book(title="Control Systems", author="Nagrath & Gopal", publisher="NewAge", year=2014, category="Electronics", copies=4),
        Book(title="Microprocessors and Interfacing", author="Douglas V Hall", publisher="Tata McGraw-Hill", year=2015, category="Electronics", copies=3),
        Book(title="Artificial Intelligence: A Modern Approach", author="Russell & Norvig", publisher="Pearson", year=2020, category="Computer Science", copies=4),
        Book(title="Machine Learning", author="Tom M. Mitchell", publisher="McGraw-Hill", year=2017, category="Computer Science", copies=4),
        Book(title="Embedded Systems", author="Raj Kamal", publisher="McGraw-Hill", year=2016, category="Electronics", copies=3),
        Book(title="Software Engineering", author="Ian Sommerville", publisher="Pearson", year=2015, category="Computer Science", copies=5),
        Book(title="Probability & Statistics for Engineers", author="Hogg & Craig", publisher="Prentice Hall", year=2014, category="Mathematics", copies=4),
        Book(title="Numerical Methods", author="S. S. Sastry", publisher="PHI", year=2018, category="Mathematics", copies=3),
        Book(title="Computer Architecture", author="Hennessy & Patterson", publisher="Morgan Kaufmann", year=2014, category="Computer Science", copies=4),
        Book(title="VLSI Design", author="Wayne Wolf", publisher="Pearson", year=2016, category="Electronics", copies=3),
        Book(title="Finite Element Analysis", author="R. D. Cook", publisher="Wiley", year=2010, category="Mechanical", copies=2),
        Book(title="Digital Communication", author="John Proakis", publisher="McGraw-Hill", year=2011, category="Electronics", copies=3),
    ]

    DataStore.save_books(samples)

    users = [
        User(name="Arjun Sharma", email="arjun.sharma@itcollege.ac.in", roll_no="IT21B001", contact="+91-9999900001"),
        User(name="Neha Singh", email="neha.singh@itcollege.ac.in", roll_no="IT21B002", contact="+91-9999900002"),
        User(name="Rohit Kumar", email="rohit.kumar@itcollege.ac.in", roll_no="IT21B003", contact="+91-9999900003"),
        User(name="Priya Verma", email="priya.verma@itcollege.ac.in", roll_no="IT21B004", contact="+91-9999900004"),
        User(name="Siddharth Gupta", email="siddharth.gupta@itcollege.ac.in", roll_no="IT21B005", contact="+91-9999900005"),
        User(name="Pooja Kaur", email="pooja.kaur@itcollege.ac.in", roll_no="IT21B006", contact="+91-9999900006"),
        User(name="Vikram Patel", email="vikram.patel@itcollege.ac.in", roll_no="IT21B007", contact="+91-9999900007"),
        User(name="Ankita Rao", email="ankita.rao@itcollege.ac.in", roll_no="IT21B008", contact="+91-9999900008"),
        User(name="Manish Yadav", email="manish.yadav@itcollege.ac.in", roll_no="IT21B009", contact="+91-9999900009"),
        User(name="Kavita Joshi", email="kavita.joshi@itcollege.ac.in", roll_no="IT21B010", contact="+91-9999900010"),
        User(name="Suresh Reddy", email="suresh.reddy@itcollege.ac.in", roll_no="IT21B011", contact="+91-9999900011"),
        User(name="Divya Nair", email="divya.nair@itcollege.ac.in", roll_no="IT21B012", contact="+91-9999900012"),
        User(name="Amit Gupta", email="amit.gupta@itcollege.ac.in", roll_no="IT21B013", contact="+91-9999900013"),
        User(name="Ritu Mehra", email="ritu.mehra@itcollege.ac.in", roll_no="IT21B014", contact="+91-9999900014"),
        User(name="Karan Singh", email="karan.singh@itcollege.ac.in", roll_no="IT21B015", contact="+91-9999900015"),
        User(name="Meera Iyer", email="meera.iyer@itcollege.ac.in", roll_no="IT21B016", contact="+91-9999900016"),
        User(name="Sahil Sharma", email="sahil.sharma@itcollege.ac.in", roll_no="IT21B017", contact="+91-9999900017"),
        User(name="Rina Das", email="rina.das@itcollege.ac.in", roll_no="IT21B018", contact="+91-9999900018"),
        User(name="Gaurav Jain", email="gaurav.jain@itcollege.ac.in", roll_no="IT21B019", contact="+91-9999900019"),
        User(name="Tina Kapoor", email="tina.kapoor@itcollege.ac.in", roll_no="IT21B020", contact="+91-9999900020"),
    ]

    DataStore.save_users(users)
