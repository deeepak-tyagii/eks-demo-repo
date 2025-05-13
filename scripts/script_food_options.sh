#!/usr/bin/env bash

# Declare an array
declare -a lunch_options

# Set working directory and file path
work_dir="$(dirname "$(readlink -f "$0")")"
food_places="${work_dir}/food_places.txt"

# Terminate with error message and optional exit code
terminate() {
  local -r msg="${1}"
  local -r code="${2:-150}"
  echo "${msg}" >&2
  exit "${code}"
}

# Exit if file doesn't exist
if [[ ! -f "${food_places}" ]]; then
  terminate "Error: food_places.txt file doesn't exist" 150
fi

# Load lines into array
function fillout_array() {
  mapfile -t lunch_options < "${food_places}"

  # Check if array is empty
  if [[ "${#lunch_options[@]}" -eq 0 ]]; then
    terminate "Error: food_places.txt is empty" 151
  fi
}

update_options() {
	if [[ "${#lunch_options[@]}" -eq 0 ]]; then
		: > "${food_places}"
	else
	        printf "%s\n" "${lunch_options[@]}" > "${food_places}"
	fi
}

# Call the function
fillout_array

index=$((RANDOM % "${#lunch_options[@]}"))

echo "${lunch_options[${index}]}"

unset "lunch_options[${index}]"

update_options
