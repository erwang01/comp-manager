
from manager import Competitor


def register_competitor() -> Competitor:
    """Registers a competitor, querying the user as needed."""
    name = input("Competitor name: ")
    email = input("Competitor email: ")
    phone = input("Competitor phone number: ")
    return Competitor(name, email, phone)


if __name__ == "__main__":
    register_competitor()