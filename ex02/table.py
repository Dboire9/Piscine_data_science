import psycopg2
import csv

def main():
	f_to_open = "data_2022_dec"
	csv_file_path = "../customer/" + f_to_open + ".csv"
	with open(csv_file_path, "r") as f:
		reader = csv.reader(f)
		columns = next(reader)
		rows = list(reader)
	create_table(f_to_open, columns, rows)

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