if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    
    # check how many trips have 0 passengers.
    zero_passengers_amt = data['passenger_count'].isin([0]).sum()
    print(f'Removed rows with 0 passengers: {zero_passengers_amt}')

    # return data where there are more than 0 passengers.
    return data[data['passenger_count'] > 0]


# test: ensure there are no records with 0 passengers.
@test
def test_output(output, *args) -> None:
    assert output['passenger_count'].isin([0]).sum() == 0 , 'There are rides with 0 passengers present'
