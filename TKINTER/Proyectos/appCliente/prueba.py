#usr/bin/python
import cx_Oracle
conexion = cx_Oracle.connect('ventas/ventas@prod')
cursor = conexion.cursor()
cursor.execute("select * from clientes where cli_idclie='008033'")
for i in cursor:
	print i[5]
