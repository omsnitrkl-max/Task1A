# main.py
import os
from script import analyze_arena

# ==========================================
# MAIN DRIVER FILE
# ==========================================

TEST_IMAGE = "Task1/Task1A/Task1A-a/Test_images/arena_1.png"

def main():

    # Check if image exists
    if not os.path.exists(TEST_IMAGE):

        print(f"Error: {TEST_IMAGE} not found.")
        return

    # Run student solution
    result = analyze_arena(TEST_IMAGE)

    # Print formatted output
    print("\n========== DETECTED OUTPUT ==========\n")

    if not result:

        print("No output returned.")

    else:

        for key, value in result.items():

            if key == "special_cells":

                print("special_cells:")

                for coord, zone in value.items():
                    print(f"  {coord} : {zone}")

            else:
                print(f"{key} : {value}")

    print("\n=====================================\n")


if __name__ == "__main__":
    main()

