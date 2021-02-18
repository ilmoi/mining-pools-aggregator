echo "==================================="
echo "Generating initial lists"
echo "==================================="
pipenv run python generate_lists.py

echo "==================================="
echo "Generating IPs"
echo "==================================="
pipenv run python generate_ips_from_lists.py

# this step is necessary coz we now have updated IP lists from previous step that we want to include
echo "==================================="
echo "Re-generating lists with updated IPs"
echo "==================================="
pipenv run python generate_lists.py

echo "==================================="
echo "Generating hosts"
echo "==================================="
pipenv run python generate_hosts.py

echo "==================================="
echo "ALL DONE. 🤘"
echo "==================================="
