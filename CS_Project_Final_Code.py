import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

def plot_vi_graph(readings_forward, readings_reverse):
    # Plot V-I graph
    plt.scatter(readings_forward[:, 0], readings_forward[:, 1], label='Forward Bias')
    plt.scatter(-readings_reverse[:, 0], -readings_reverse[:, 1], label='Reverse Bias')

    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (I)')
    plt.title('P-N Junction Diode V-I Graph')
    plt.axhline(y=0, color='black', linewidth=0.5)
    plt.axvline(x=0, color='black', linewidth=0.5)
    plt.legend()
    plt.grid(True)
    plt.show()

def collect_readings(graph_type, num_readings):
    print(f"Enter readings for {graph_type}:")

    readings = []
    for i in range(num_readings):
        # Adjust the column names based on the selected graph type
        column1_name, column2_name = get_column_names(graph_type)

        value1 = float(input(f"Enter {column1_name} reading {i + 1}: "))
        value2 = float(input(f"Enter {column2_name} reading {i + 1}: "))
        readings.append([value1, value2])

    return np.array(readings)

def fetch_data_from_database(database_name, table_name, condition=None):
    connection = mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="new_password",
        database=database_name
    )
    
    cursor = connection.cursor()

    query = f"SELECT * FROM {table_name}"
    if condition:
        query += f" WHERE {condition}"

    cursor.execute(query)
    data = np.array(cursor.fetchall())

    connection.close()

    # Reshape the array if it's one-dimensional
    if data.ndim == 1:
        data = data.reshape(1, -1)

    return data

def get_column_names(graph_type):
    if graph_type == "V-I Graph of wire":
        return "Voltmeter", "Ammeter"
    elif graph_type == "Prism: Angle of Incidence vs Angle of Deviation":
        return "Angle_of_Incidence", "Angle_of_Deviation"
    elif graph_type == "Convex Lens: Object Distance vs Image Distance":
        return "Object_Distance", "Image_Distance"
    elif graph_type == "Concave Mirror: Object Distance vs Image Distance":
        return "Object_Distance", "Image_Distance"
    elif "P-N Junction Diode" in graph_type:
        return "Voltage", "Current"
    else:
        raise ValueError(f"Unsupported graph type: {graph_type}")

def main():
    # Ask the user for their name
    user_name = input("Enter your name: ")
    print(f"Hello, {user_name}!")

    while True:
        # Ask the user to select the type of graph
        graph_types = [
            "V-I Graph of wire",
            "Prism: Angle of Incidence vs Angle of Deviation",
            "Convex Lens: Object Distance vs Image Distance",
            "Concave Mirror: Object Distance vs Image Distance",
            "P-N Junction Diode: V-I"
        ]

        print("Select the type of graph:")
        for i, graph_type in enumerate(graph_types, start=1):
            print(f"{i}. {graph_type}")

        selected_index = int(input("Enter the number corresponding to YOUR desired graph: ")) - 1
        selected_graph_type = graph_types[selected_index]

        use_default_values = input("Do you want to use default values from the database? (yes/no): ").lower() == 'yes'

        if use_default_values:
            if "P-N Junction Diode" in selected_graph_type:
                forward_readings = fetch_data_from_database("pndiode", "forwardbias")
                reverse_readings = fetch_data_from_database("pndiode", "reversebias")
                plot_vi_graph(forward_readings, reverse_readings)
            else:
                if selected_graph_type == "V-I Graph of wire":
                    readings = fetch_data_from_database("v_i_graph", "graphdata")
                elif selected_graph_type == "Prism: Angle of Incidence vs Angle of Deviation":
                    readings = fetch_data_from_database("prism", "prismdata")
                elif selected_graph_type == "Convex Lens: Object Distance vs Image Distance":
                    readings = fetch_data_from_database("convexlens", "lensdata")
                elif selected_graph_type == "Concave Mirror: Object Distance vs Image Distance":
                    readings = fetch_data_from_database("concavemirror", "mirrordata")
                

        else:
            if selected_graph_type == "P-N Junction Diode: V-I":
                forward_readings = collect_readings("P-N Junction Diode (Forward Bias)", num_readings=6)
                reverse_readings = collect_readings("P-N Junction Diode (Reverse Bias)", num_readings=6)
                readings = np.vstack([forward_readings, reverse_readings])
            else:
                # Guide the user on filling the required columns and rows
                print(f"Please provide the following readings for {selected_graph_type}:")
                if selected_graph_type == "V-I Graph of wire":
                    print("Columns: Voltmeter, Ammeter")
                    print("Rows (provide 5 sets):")
                elif selected_graph_type == "Prism: Angle of Incidence vs Angle of Deviation":
                    print("Columns: Angle_of_Incidence, Angle_of_Deviation")
                    print("Rows (provide 6 sets):")
                elif selected_graph_type == "Convex Lens: Object Distance vs Image Distance":
                    print("Columns: Object_Distance, Image_Distance")
                    print("Rows (provide 5 sets):")
                elif selected_graph_type == "Concave Mirror: Object Distance vs Image Distance":
                    print("Columns: Object_Distance, Image_Distance")
                    print("Rows (provide 5 sets):")

                readings = collect_readings(selected_graph_type, num_readings=6)  # Adjust the num_readings as needed

        # Plot the graph
        if selected_graph_type == "P-N Junction Diode: V-I":
            plot_vi_graph(forward_readings, reverse_readings)
        else:
            plt.scatter(readings[:, 0], readings[:, 1])
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.title(f'{selected_graph_type} Graph')
            plt.axhline(y=0, color='black', linewidth=0.5)
            plt.axvline(x=0, color='black', linewidth=0.5)
            plt.grid(True)
            plt.show()

        # Ask the user if they want to generate more graphs
        generate_more = input("Do you want to generate more graphs? (yes/no): ").lower()
        if generate_more != 'yes':
            print(f"Thank you, {user_name}, for using our service. Goodbye!")
            break

if __name__ == "__main__":
    main()

                
