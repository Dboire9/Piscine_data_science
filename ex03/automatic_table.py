import psycopg2
import csv
import os

def main():
	customer_folder = "../customer/"
	
	# Get all CSV files in the customer folder
	csv_files = [f for f in os.listdir(customer_folder) if f.endswith(".csv")]
	
	for csv_file in csv_files:
		csv_file_path = os.path.join(customer_folder, csv_file)
		table_name = os.path.splitext(csv_file)[0]
		
		with open(csv_file_path, "r") as f:
			reader = csv.reader(f)
			columns = next(reader) 
			rows = list(reader)
		
		create_table(table_name, columns, rows)

def create_table(name, columns, rows):
	column_definitions = ", ".join([f"{col} TEXT" for col in columns])
	create_table_command = f"""
	CREATE TABLE IF NOT EXISTS {name} (
		{column_definitions}
	)
	"""
	placeholders = ", ".join(["%s"] * len(columns))
	insert_command = f"INSERT INTO {name} ({', '.join(columns)}) VALUES ({placeholders})"
	
	conn = None
	try:
		conn = psycopg2.connect(
		dbname="piscineds",
		user="dboire",
		password="mysecretpassword",
		host="localhost",
		port="5432"
		)
		cur = conn.cursor()
		cur.execute(create_table_command)
		conn.commit()
		cur.executemany(insert_command, rows)
		conn.commit()
		
		print(f"Table '{name}' created and data inserted successfully.")
	
	except (Exception, psycopg2.DatabaseError) as error:
		print(f"Error: {error}")
	
	finally:
		if conn:
			cur.close()
			conn.close()




if __name__ == "__main__":
	main()