for test_file in $(find|grep test_|egrep -v '~|pyc'); do
    echo $test_file;
    python "${test_file:2}";
done
