#!/bin/bash
what=$1
var=$2
submit=$3

# Some constants
# check if we want to plot or make cards
if [[ $what == *"card"* ]]; then
    # Want to make cards
    if [[ $what == *"gen"* ]]; then
        # Cards at GEN level
        echo
        extra="gen"
    fi

    for year in 2016 2016APV 2017 2018 ; do 
        echo ====== $year ===== 
        if [[ ! $submit == "do-submit" ]]; then 
            echo " >> Printing command "
            python ttW_multilepton/make_cards_new.py 3l_$var ${year} 3l $var diff $extra
        else
            echo " >> Submitting command "
            python ttW_multilepton/make_cards_new.py 3l_$var ${year} 3l $var diff $extra | bash
            echo " >> Job submitted "
        fi
        echo ==================
    done

elif [[ $what == *"plot"* ]]; then
    if [[ $what == *"gen"* ]]; then
        # Cards at GEN level
        echo
        extra="_genlevel"
    fi
    echo ====== $var ===== 
    if [[ ! $submit == "do-submit" ]]; then 
        echo " >> Printing command "
        python ttW_multilepton/ttW_plots.py $var all 3l_tight_data_frdata_diff_unc_blinddata$extra --sP $var
    else
        echo " >> Submitting command "
        python ttW_multilepton/ttW_plots.py $var all 3l_tight_data_frdata_diff_unc_blinddata$extra --sP $var | bash
        echo " >> Job submitted "
    fi
    echo ================== 
fi
