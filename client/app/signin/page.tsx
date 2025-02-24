export default function SignInPage() {
    return (
        <div>
            <h1>Sign in</h1>
            <form>
                <label className="text-blue-200">
                    Email
                    <input type="email" />
                </label>
                <label>
                    Password
                    <input type="password" />
                </label>
                <button type="submit">Sign in</button>
            </form>
        </div>
    )
}