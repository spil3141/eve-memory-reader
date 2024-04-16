#include <stdio.h>
#include <eve-memory-reader.h>

int save_to_file_as_json(const char* file_name, const char* json);
void refresh_ui_tree();

char* UITreeJson = NULL;

int main()
{
	initialize();

	read_ui_trees();

	UITreeJson = get_ui_json();

	save_to_file_as_json("ui_tree_1.json", UITreeJson);

	system("pause");

	read_ui_trees();

	UITreeJson = get_ui_json();
	
	save_to_file_as_json("ui_tree_2.json", UITreeJson);

	free_ui_json();

	system("pause");
}

int save_to_file_as_json(const char* file_name, const char* json)
{
	FILE* file = fopen(file_name, "w");
	if (file == NULL)
	{
		return 0;
	}

	fprintf(file, "%s", json);
	fclose(file);
	return 1;
}