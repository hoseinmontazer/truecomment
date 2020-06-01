<?xml version="1.0"?>
<mysqldump xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<database name="url">
	<table_structure name="comment">
		<field Field="comment" Type="varchar(1000)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="id" Type="int" Null="NO" Key="" Extra="" Comment="" />
		<options Name="comment" Engine="InnoDB" Version="10" Row_format="Dynamic" Rows="0" Avg_row_length="0" Data_length="16384" Max_data_length="0" Index_length="0" Data_free="0" Create_time="2020-06-01 13:42:44" Collation="utf32_persian_ci" Create_options="" Comment="" />
	</table_structure>
	<table_structure name="url">
		<field Field="url" Type="varchar(300)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="id" Type="int" Null="NO" Key="PRI" Extra="auto_increment" Comment="" />
		<key Table="url" Non_unique="0" Key_name="PRIMARY" Seq_in_index="1" Column_name="id" Collation="A" Cardinality="0" Null="" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<options Name="url" Engine="InnoDB" Version="10" Row_format="Dynamic" Rows="0" Avg_row_length="0" Data_length="16384" Max_data_length="0" Index_length="0" Data_free="0" Auto_increment="1" Create_time="2020-06-01 13:42:08" Collation="utf32_persian_ci" Create_options="" Comment="" />
	</table_structure>
</database>
</mysqldump>
