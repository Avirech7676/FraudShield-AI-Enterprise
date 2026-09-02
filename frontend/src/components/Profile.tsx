export default function Profile() {
  const username = localStorage.getItem("username");

  const role = localStorage.getItem("role");

  return (
    <div>
      <h2>User Profile</h2>

      <p>Username : {username}</p>

      <p>Role : {role}</p>
    </div>
  );
}
