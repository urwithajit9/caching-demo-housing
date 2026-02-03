# This fires 50 requests as fast as possible in the background
for i in {1..50}; do 
  curl -o /dev/null -s -w "Request $i: %{time_total}s\n" http://localhost:8000/api/properties/ & 
done; wait
