class NuclideProperties:
    def __init__(self) :
        self.x = 0
nuclides_properties = {
    ("U", 235) : NuclideProperties
}
def main() -> None:
    print("Hello from atomics!")
