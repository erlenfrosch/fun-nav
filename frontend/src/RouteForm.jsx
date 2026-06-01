export default function RouteForm({ onSubmit, loading }) {
  function handleSubmit(e) {
    e.preventDefault()
    const data = new FormData(e.target)
    onSubmit({
      from_lat: parseFloat(data.get('from_lat')),
      from_lon: parseFloat(data.get('from_lon')),
      to_lat: parseFloat(data.get('to_lat')),
      to_lon: parseFloat(data.get('to_lon')),
    })
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'flex-end' }}>
      <fieldset style={{ border: '1px solid #ccc', padding: '0.5rem', borderRadius: '4px' }}>
        <legend>Start</legend>
        <label>
          Lat <input name="from_lat" type="number" step="any" defaultValue="47.13" required style={{ width: '90px' }} />
        </label>{' '}
        <label>
          Lon <input name="from_lon" type="number" step="any" defaultValue="9.52" required style={{ width: '90px' }} />
        </label>
      </fieldset>
      <fieldset style={{ border: '1px solid #ccc', padding: '0.5rem', borderRadius: '4px' }}>
        <legend>Ziel</legend>
        <label>
          Lat <input name="to_lat" type="number" step="any" defaultValue="47.05" required style={{ width: '90px' }} />
        </label>{' '}
        <label>
          Lon <input name="to_lon" type="number" step="any" defaultValue="9.73" required style={{ width: '90px' }} />
        </label>
      </fieldset>
      <button type="submit" disabled={loading} style={{ padding: '0.5rem 1rem' }}>
        {loading ? 'Berechne…' : 'Route berechnen'}
      </button>
    </form>
  )
}
