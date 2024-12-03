awk -F, 'NR==1 {print $0",insurance_type"; next} 
         NR>1 {
            # Assign insurance type based on age
            if ($4 >= 18 && $4 <= 40) {
                insurance_type = "Bronze";
            } else if ($4 > 40 && $4 <= 60) {
                insurance_type = "Silver";
            } else {
                insurance_type = "Gold";
            }
            print $0","insurance_type;
        }' ms_data.csv > ms_data_with_insurance.csv
echo -e "Bronze\nSilver\nGold" > insurance.lst
echo "Total rows with header:"
wc -l ms_data_with_insurance.csv
echo "First few rows with insurance types:"
head ms_data_with_insurance.csv
