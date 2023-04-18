
rule update_test_data:
    input: 
        "src/update_test_data.py"
    output:
        "tests/data/game_data.html",
        "tests/data/teams_data.html"
    shell:
        "python {input} {output}"