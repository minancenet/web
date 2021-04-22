def keyRequired(parser):
  """Helper function for requireing an API key."""
  # Implement actual API key validation "0" is for testing purposes

  parser.add_argument(
    "key",
    type=str,
    required=True,
    choices=("0"),
    help="Invalid field [key]",
  )