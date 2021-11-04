a=$(kubectl get pods -n ingress-nginx --no-headers -o custom-columns=":metadata.name")
IFS=' ' read -r -a array <<< "abc dacmdp cpsdp"
echo $array
for element in "${array[@]}"
do
    # echo "$element"
done